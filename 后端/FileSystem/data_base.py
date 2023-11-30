import uuid
from datetime import datetime
from random import sample

from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, or_, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash

from configs import SQLALCHEMY_DATABASE_URI, SAMPLE_FIELD, identity_permission_code_map, COLLECTIONS_FOLDER_URL, \
    SCHEDULER_TIMEZONE
from utils.my_email import templates, mail
from utils.scheduler import scheduler, one_day_forward

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI)#,echo=configs.SQLALCHEMY_ECHO
Session = sessionmaker(bind=engine)
session = Session()

def remind_email(collection):
    email_list=[student.email for student in [User.get_user(student_id) for student_id in CollectionRecord.get_unfinished_student_id_list(collection.collection_id)]]
    mail('作业提醒', email_list, templates('remind')
         .replace('CLASS_NAME', collection.class_name)
         .replace('COLLECTION_NAME',collection.collection_name)
         .replace('COLLECTION_END_TIME',collection.collection_end_time.strftime('%Y-%m-%d %H:%M:%S')))

class TypeCast:
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    def to_json(self, all_vendors):
        v = [ven.to_dict() for ven in all_vendors]
        return v
    Base.to_dict = to_dict
    Base.to_json = to_json

#未激活用户表
class User_n(Base):
    __tablename__ = 'user_n'
    id = Column(String(32), nullable=False)
    name = Column(String(32), nullable=False)
    password = Column(String(110), nullable=False)
    email = Column(String(32), nullable=False)
    academy = Column(String(32), nullable=False)
    identity = Column(String(32), nullable=False)
    activate_code = Column(String(110), primary_key=True, nullable=False)
    activate_permission = Column(Boolean, nullable=False)
    def __init__(self, id, name, password, email, academy, identity, activate_code):
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        self.academy = academy
        self.identity = identity
        self.activate_code = activate_code
        if identity=='student':
            self.activate_permission = True
        else:
            self.activate_permission = False

    @staticmethod
    def new_from_user(user, activate_code):
        user_n = User_n(user.id, user.name, user.password, user.email, user.academy, user.identity, activate_code)
        user_n.activate_permission = True
        session.add(user_n)
        session.query(User).filter(User.id == user.id).delete()
        session.commit()
    @staticmethod
    def activate_permission_user(activate_code):
        # 验证准许激活状态与激活码
        user_query = session.query(User_n).filter(User_n.activate_code == activate_code)
        if user_query.first():  # 激活码验证正确
            user_query.update({'activate_permission': True}, synchronize_session=False)
            session.commit()
        User_n.activate_user()

    @staticmethod
    def activate_user():
        query_user = session.query(User_n).filter(User_n.activate_permission == True, User_n.activate_code == '').first()
        if query_user:  # 顺利验证
            session.add(User(query_user))
            session.query(User_n).filter(User_n.id == query_user.id).delete()
        session.commit()
#已激活用户表
class User(Base):
    __tablename__ = 'user'
    id = Column(String(32), primary_key=True, nullable=False)
    name = Column(String(32), nullable=False)
    password = Column(String(110), nullable=False)
    email = Column(String(32), nullable=False)
    academy = Column(String(32), nullable=False)
    identity = Column(String(32), nullable=False)
    def __init__(self, user_n):
        self.id = user_n.id
        self.name = user_n.name
        self.password = user_n.password
        self.email = user_n.email
        self.academy = user_n.academy
        self.identity = user_n.identity

    def get_permission_code(self):
        permission_code = identity_permission_code_map[self.identity]
        if self.identity=='student' and session.query(Class).filter(Class.permission_students_id.like(f'%{self.id}%')).first():
            permission_code = permission_code | identity_permission_code_map['collector']
        elif self.identity=='teacher' and session.query(Class).filter(Class.teacher_id == self.id).first():
            permission_code = permission_code | identity_permission_code_map['collector']
        return permission_code

    def reset_password(self):
        new_password = self.id+'_'+''.join(sample(SAMPLE_FIELD, 6))
        session.query(User).filter(User.id == self.id).update({'password': generate_password_hash(new_password)})
        session.commit()
        return new_password
    def delete(self):
        session.query(User).filter(User.id == self.id).delete()
        session.commit()
    def update(self,field,data):
        if field=='password':
            data=generate_password_hash(data)
        session.query(User).filter(User.id == self.id).update({field: data})
        session.commit()
    @staticmethod
    def id_and_name_json_list(id_list, id_field='id', name_field='name'):
        return [{id_field:user.id,name_field:user.name} for user in
                    session.query(User).filter(User.id.in_(id_list)).all()]

    #查询用户对象
    @staticmethod
    def get_user(id):
        return session.query(User).filter(User.id == id).first()

    @staticmethod
    def login(id, password):
        user = session.query(User).filter(or_(User.id == id, User.email == id))
        print(user.first())
        if user.first():
            return user.filter(check_password_hash(user.first().password,password)).first()
        else:
            return None

    # ###### 教师 ###### 教师 ###### 教师 ######
    # 根据教师id获取下属的班级列表
    @staticmethod
    def teacher_get_class_list(teacher_id):
        class_list = [class_id[0] for class_id in
                      session.query(Class.id).filter(Class.teacher_id == teacher_id).all()]
        class_list = [Class.get_class_info(class_id) for class_id in class_list]
        return class_list

    # ###### 学生 ###### 学生 ###### 学生 ######
    # 根据学生id获取被授权的班级列表
    @staticmethod
    def student_get_permission_class_list(student_id):
        class_list = [class_id[0] for class_id in
                      session.query(Class.id).filter(Class.permission_students_id.like(f'%{student_id}%')).all()]
        class_list = [Class.get_class_info(class_id) for class_id in class_list]
        return class_list

    # ###### 学生 ###### 学生 ###### 学生 ######
    # 根据学生id获取所在的班级列表
    @staticmethod
    def student_get_class_id_list(student_id):
        not_include_class_list = set(class_id[0] for class_id in session.query(ClassStudentMap.class_id).filter(and_(ClassStudentMap.student_id==student_id,ClassStudentMap.flag==False)).all())
        base_class_list = set(class_id[0] for class_id in session.query(ClassStudentMap.class_id).filter(ClassStudentMap.student_id == student_id).all())

        complex_class_id_list = session.query(Class).filter(Class.component_classes_id!='').all()
        complex_class_id_list = set(class_.id for class_ in filter(lambda class_: set(class_.component_classes_id.split())&base_class_list,complex_class_id_list))
        #交集
        class_list = base_class_list | complex_class_id_list
        class_list = class_list - not_include_class_list
        return list(class_list)

    @staticmethod
    def student_get_class_list(student_id):
        class_list = User.student_get_class_id_list(student_id)
        class_list = [Class.get_class_info(class_id) for class_id in class_list]
        return class_list

    # ###### 管理员 ###### 管理员 ###### 管理员 ######
    # 根据管理id获取管理的用户
    @staticmethod
    def admin_get_user_list(admin_id):
        user = User.get_user(admin_id)
        user_list=[]
        if user.identity=='super_admin':
            users = session.query(User).filter(User.identity.notin_(['super_admin'])).all()
        elif user.identity=='admin':
            users = session.query(User).filter(User.academy==user.academy).filter(User.identity.notin_(['admin','super_admin'])).all()
        for u in users:
            u = u.to_dict()
            u.pop('password')
            user_list.append(u)
        return user_list

    def get_unactivated_user(self):
        if self.identity=='admin':
            return [user.to_dict() for user in session.query(User_n).filter(User_n.activate_permission == False,User_n.academy==self.academy).all()]
        elif self.identity=='super_admin':
            return [user.to_dict() for user in session.query(User_n).filter(User_n.activate_permission == False).all()]
class Academy(Base):
    __tablename__ = 'academy'
    name = Column(String(255), primary_key=True, nullable=False)
    regist_view = Column(String(255), nullable=False)

    #获取学院列表
    @staticmethod
    def get_academy_list(identity):
        identity = '%'+identity+'%'
        return [{'label':a.name,'value':a.name} for a in session.query(Academy).filter(Academy.regist_view.like(identity)).all()]

class Class(Base):
    __tablename__ = 'class'
    id = Column(String(32), primary_key=True, nullable=False)
    name = Column(String(32), nullable=False)
    students_amount = Column(Integer)
    teacher_id = Column(String(32), nullable=False)
    teacher_name = Column(String(32), nullable=False)
    academy = Column(String(32), nullable=False)
    permission_students_id = Column(String(255))
    component_classes_id = Column(String(255))
    cover = Column(String(32))

    def __init__(self,name,teacher_id):
        teacher = User.get_user(teacher_id)
        self.id = ''.join(sample(SAMPLE_FIELD, 8))
        self.name = name
        self.students_amount = 0
        self.teacher_id = teacher.id
        self.teacher_name = teacher.name
        self.academy = teacher.academy
        self.permission_students_id = ''
        self.component_class_id = ''
        self.cover = 'template:01//'

    @staticmethod
    def get_class(class_id):
        return session.query(Class).filter(Class.id == class_id).first()

    @staticmethod
    def new_class(class_name, teacher_id):
        session.add(Class(class_name,teacher_id))
        session.commit()

    @staticmethod
    def get_class_info(class_id):
        class_ = Class.get_class(class_id)
        all_students = User.id_and_name_json_list(Class.get_all_students_of_class(class_id))
        students_amount = len(all_students)
        Class.update(class_id,'students_amount',students_amount)
        return {
            'id' : class_.id,
            'name' : class_.name,
            'teacher_id' : class_.teacher_id,
            'teacher_name' : class_.teacher_name,
            'academy' : class_.academy,
            'permission_students_id' : class_.permission_students_id.split(',') if class_.permission_students_id else [],
            'component_classes' : class_.get_component_classes(),
            'cover' : class_.cover,

            'all_students': all_students,
            'students_amount': students_amount,
            'except_students': User.id_and_name_json_list(class_.get_except_students_of_class())
        }
    @staticmethod
    def get_cover(class_id):  # 返回id  list
        return session.query(Class.cover).filter(Class.id == class_id).first()[0]

    # 获取下属的组成班列表
    def get_component_classes(self):#返回id  list
        component_classes = self.component_classes_id.split(',') if self.component_classes_id else []
        if component_classes:
            return [component_class.id for component_class in
                    session.query(Class).filter(Class.id.in_(component_classes)).all()]
        else:
            return []

    @staticmethod
    def update(class_id, field, data):
        class_ = Class.get_class(class_id)
        if class_:
            session.query(Class).filter(Class.id == class_id).update({field: data})
            session.commit()

    # 根据班级id获取学生列表
    def get_students_of_class(self):  # 返回id  list
        return [student[0] for student in
                session.query(ClassStudentMap.student_id).filter(ClassStudentMap.class_id == self.id).filter(
                    ClassStudentMap.flag == True).all()]

    # 根据班级id获取排除的学生列表
    def get_except_students_of_class(self):  # 返回id  list
        return [student[0] for student in
                session.query(ClassStudentMap.student_id).filter(ClassStudentMap.class_id == self.id).filter(
                    ClassStudentMap.flag == False).all()]

    # 根据班级id获取所属所有学生的列表(包括子班级的)
    @staticmethod
    def get_all_students_of_class(class_id, first_time=True):  # 返回id  list
        students = []
        class_ = Class.get_class(class_id)
        # 查看组成班
        if class_.component_classes_id:
            for component_class_id in class_.component_classes_id.split(','):
                # 获得组成班的所有学生, 并且递归
                students.extend(Class.get_all_students_of_class(component_class_id, first_time=False))
        # 加上自身基础的学生
        students.extend(class_.get_students_of_class())
        # 去重并剔除不要的学生
        if first_time:
            except_students = class_.get_except_students_of_class()
            students = list(set(students) - set(except_students))
        return students

    # 调整班级学生
    @staticmethod
    def student_adjust(class_id, student_id_list, flag):
        class_ = Class.get_class(class_id)
        if flag==False:
            permission_students_list = class_.permission_students_id.split(',') if class_.permission_students_id else []
        student_adjust_list=[ClassStudentMap(flag, class_id, student_id) for student_id in student_id_list]
        adjust_num=0
        for class_Student_map in student_adjust_list:
            # 已授权的学生一并解除授权
            if flag==False and class_Student_map.student_id in permission_students_list:
                permission_students_list.remove(class_Student_map.student_id)
                Class.update(class_id,'permission_students_id',','.join(permission_students_list) if permission_students_list else '')
            adjust_num = adjust_num+(1 if adjust_num+class_Student_map.flag else 0)

            session.merge(class_Student_map)
        session.commit()

        Class.update(class_id, 'students_amount', Class.get_class(class_id).students_amount+adjust_num)

    def delete(self):
        class_list = dict(session.query(Class.id,Class.component_classes_id).filter(Class.component_classes_id.like(f"%{self.id}%")).all())
        for key, val in class_list.items():
            val = val.replace(self.id+',', '')
            val = val.replace(','+self.id, '')
            val = val.replace(self.id, '')
            session.query(Class).filter(Class.id==key).update({'component_classes_id':val})
        session.query(Class).filter(Class.id==self.id).delete()
        session.query(ClassStudentMap).filter(ClassStudentMap.class_id == self.id).delete()
        collection_id = [collection_id[0] for collection_id in  session.query(Collection.collection_id).filter(Collection.class_id == self.id).all()]
        for collection in collection_id:
            Collection.delete_collection(collection)
        session.commit()

class ClassStudentMap(Base):
    __tablename__ = 'class_student_map'
    flag = Column(Boolean, nullable=False)
    class_id = Column(String(8), primary_key=True, nullable=False)
    student_id = Column(String(32), primary_key=True, nullable=False)

    def __init__(self, flag, class_id, student_id):
        self.flag = flag
        self.class_id = class_id
        self.student_id = student_id

    @staticmethod
    def student_join_class(class_id, student_id):
        if session.query(ClassStudentMap).filter(ClassStudentMap.class_id==class_id,ClassStudentMap.student_id==student_id).first():
            pass
        else:
            session.add(ClassStudentMap(True,class_id,student_id))
            session.commit()
    @staticmethod
    def student_quit_class(class_id, student_id):
        Class.student_adjust(class_id,[student_id],False)

class Collection(Base):
    __tablename__ = 'collection'
    collection_id = Column(String(36), primary_key=True, nullable=False)
    collection_name = Column(String(255), nullable=False)
    collection_info = Column(String(255))
    collection_start_time = Column(DateTime, nullable=False)
    collection_end_time = Column(DateTime, nullable=False)
    collection_items_amount = Column(Integer, nullable=False)
    class_id = Column(String(8), nullable=False)
    class_name = Column(String(32), nullable=False)

    def __init__(self, form):
        self.collection_id = uuid.uuid1()
        self.collection_name = form.get('collection_name')
        self.collection_info = form.get('collection_info')
        self.class_id = form.get('class_id')
        self.class_name = form.get('class_name')
        self.collection_start_time = form.get('collection_start_time')
        self.collection_end_time = form.get('collection_end_time')
        self.collection_items_amount = form.get('collection_items_amount')

    @staticmethod
    def new_collection(form):
        collection=Collection(form)
        session.add(collection)
        session.commit()
        scheduler.add_job(remind_email, id=collection.collection_id, trigger='date', run_date=one_day_forward(collection.collection_end_time), args=[collection],timezone=SCHEDULER_TIMEZONE)
        return collection.collection_id
    @staticmethod
    def delete_collection(collection_id):
        session.query(Collection).filter(Collection.collection_id == collection_id).delete()
        session.query(CollectionItems).filter(CollectionItems.collection_id == collection_id).delete()
        session.query(CollectionRecord).filter(CollectionRecord.collection_id == collection_id).delete()
        session.commit()
        try:
            scheduler.remove_job(collection_id) # 删除定时提醒任务
        except:
            pass
    @staticmethod
    def update(collection_id, field, data):
        collection = Collection.get_collection(collection_id)
        if collection:
            session.query(Collection).filter(Collection.collection_id == collection.collection_id).update({field: data})
            session.commit()
            if field=='collection_end_time' and one_day_forward(data)>datetime.now():#更新收集结束时间则重置定时任务
                jobs=[job.id for job in scheduler.get_jobs()]
                if collection_id in jobs:
                    scheduler.reschedule_job(collection_id, jobstore=None, trigger='date', run_date=one_day_forward(data))
                else:
                    for collection in Collection.get_collections_end_in_future(one_day_=True):  # 任务截止前一天提醒
                        scheduler.add_job(remind_email, id=collection.collection_id, trigger='date',
                                          run_date=one_day_forward(collection.collection_end_time), args=[collection],
                                          timezone=SCHEDULER_TIMEZONE)
    @staticmethod
    def get_collection(collection_id):
        return session.query(Collection).filter(Collection.collection_id == collection_id).first()

    @staticmethod
    def get_collections_by_class_id(class_id):
        collections = [collection.to_dict() for collection in session.query(Collection).filter(Collection.class_id == class_id).all()]
        for collection in collections:
            submit_count = session.query(func.count(CollectionRecord.student_id)).filter(CollectionRecord.collection_id == collection['collection_id']).scalar()
            students_amount = session.query(Class.students_amount).filter(Class.id == class_id).first()[0]
            collection_progress = submit_count/collection['collection_items_amount']/students_amount*100
            collection['collection_progress'] = collection_progress
            collection['collection_start_time'] = collection['collection_start_time'].timestamp()*1000
            collection['collection_end_time'] = collection['collection_end_time'].timestamp()*1000
        return collections

    @staticmethod
    def get_student_collection_list(student_id):
        class_list = User.student_get_class_id_list(student_id)
        collection_list = [collection.to_dict() for collection in session.query(Collection).filter(Collection.class_id.in_(class_list)).all()]
        for collection in collection_list:
            collection['cover'] = Class.get_cover(collection['class_id'])
            collection['collection_start_time'] = collection['collection_start_time'].timestamp() * 1000
            collection['collection_end_time'] = collection['collection_end_time'].timestamp() * 1000
            collection['items'] = CollectionItems.get_collection_items(student_id,collection['collection_id'])
            collection['finished'] = collection['collection_items_amount']==session.query(func.count(CollectionRecord.index)).filter(
                CollectionRecord.collection_id == collection['collection_id'], CollectionRecord.student_id == student_id).scalar()
        return collection_list
    @staticmethod
    def get_collections_end_in_future(one_day_):
        if one_day_:
            return session.query(Collection).filter(Collection.collection_end_time >= one_day_forward(datetime.now())).all()
        else:
            return session.query(Collection).filter(Collection.collection_end_time >= datetime.now()).all()


class CollectionItems(Base):
    __tablename__ = 'collection_items'
    collection_id = Column(String(36), primary_key=True, nullable=False)
    index = Column(Integer, primary_key=True, nullable=False)
    info = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

    def __init__(self, collection_item):
        self.collection_id = collection_item['collection_id']
        self.index = collection_item['index']
        self.info = collection_item['info']
        self.type = collection_item['type']

    @staticmethod
    def new_collection_item(collection_item):
        session.add(CollectionItems(collection_item))
        session.commit()

    @staticmethod
    def get_collection_items(student_id,collection_id):
        items = [item.to_dict() for item in session.query(CollectionItems).filter(CollectionItems.collection_id==collection_id).all()]
        submit_record = CollectionRecord.query_submit_record(student_id, collection_id)
        for index,item in enumerate(items):
            item['exist'] = index in submit_record
        return items
    @staticmethod
    def get_collection_items_info(collection_id):
        return [info[0] for info in session.query(CollectionItems.info).filter(CollectionItems.collection_id==collection_id).order_by(CollectionItems.index).all()]


class CollectionRecord(Base):
    __tablename__ = 'collection_record'
    collection_id = Column(String(36), primary_key=True, nullable=False)
    index = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(String(32), primary_key=True, nullable=False)
    student_name = Column(String(32), primary_key=True, nullable=False)
    submit_time = Column(DateTime, nullable=False, default=datetime.now)
    submit_content = Column(String(255), nullable=False)

    def __init__(self, collection_record):
        self.collection_id = collection_record['collection_id']
        self.index = collection_record['index']
        self.student_id = collection_record['student_id']
        self.student_name = collection_record['student_name']
        self.submit_content = collection_record['submit_content']

    @staticmethod
    def new_collection_record(collection_record):
        session.add(CollectionRecord(collection_record))
        session.commit()

    @staticmethod
    def query_record(student_id, collection_id, index):
        return session.query(CollectionRecord).filter(CollectionRecord.student_id == student_id,
                                                            CollectionRecord.collection_id == collection_id,
                                                            CollectionRecord.index == index,).first()
    @staticmethod
    def query_submit_record(student_id, collection_id):
        return [index[0] for index in session.query(CollectionRecord.index).filter(CollectionRecord.collection_id==collection_id,
                                                           CollectionRecord.student_id==student_id).all()]

    @staticmethod
    def delete_record(student_id, collection_id,index):
        session.query(CollectionRecord).filter(CollectionRecord.collection_id==collection_id,
                                               CollectionRecord.student_id==student_id,
                                               CollectionRecord.index==index).delete()
        session.commit()

    @staticmethod
    def collating_record(collection_id):
        return session.query(CollectionRecord.student_id,CollectionRecord.student_name,func.count(CollectionRecord.index),func.group_concat(CollectionRecord.index)).filter(CollectionRecord.collection_id==collection_id).group_by(CollectionRecord.student_id).group_by(CollectionRecord.student_name).all()

    @staticmethod
    def get_unfinished_student_id_list(collection_id):
        collection = Collection.get_collection(collection_id)
        all_students = Class.get_all_students_of_class(collection.class_id)
        finished_students=[id_[0] for id_ in session.query(CollectionRecord.student_id).filter(CollectionRecord.collection_id==collection_id).group_by(CollectionRecord.student_id).having(func.count(CollectionRecord.index) == collection.collection_items_amount).all()]
        return list(set(all_students)-set(finished_students))