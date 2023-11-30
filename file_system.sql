/*
 Navicat Premium Data Transfer

 Source Server         : Navicat
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : file_system

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 10/05/2023 01:34:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for academy
-- ----------------------------
DROP TABLE IF EXISTS `academy`;
CREATE TABLE `academy`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '学院名称',
  `regist_view` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '注册时可见的角色范围',
  PRIMARY KEY (`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of academy
-- ----------------------------
INSERT INTO `academy` VALUES ('人文学院', 'student,teacher');
INSERT INTO `academy` VALUES ('数学与数据科学学院（软件学院）', 'student,teacher');
INSERT INTO `academy` VALUES ('物电学院', 'student,teacher');
INSERT INTO `academy` VALUES ('阳光体育学院', 'teacher');
INSERT INTO `academy` VALUES ('马克思主义学院', 'teacher');

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class`  (
  `id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '班级id',
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '班级名称',
  `students_amount` int(0) NOT NULL COMMENT '学生数量',
  `teacher_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '教师id',
  `teacher_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '教师名字',
  `academy` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '所属学院',
  `permission_students_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '授权发布收集的学生',
  `component_classes_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '组成此班级的班级的id(逗号分隔)',
  `cover` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '封面信息',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `学院外键`(`academy`) USING BTREE,
  CONSTRAINT `学院外键` FOREIGN KEY (`academy`) REFERENCES `academy` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for class_student_map
-- ----------------------------
DROP TABLE IF EXISTS `class_student_map`;
CREATE TABLE `class_student_map`  (
  `flag` tinyint(1) NOT NULL DEFAULT 1 COMMENT '标识符',
  `class_id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '班级id',
  `student_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '学生id',
  PRIMARY KEY (`class_id`, `student_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for collection
-- ----------------------------
DROP TABLE IF EXISTS `collection`;
CREATE TABLE `collection`  (
  `collection_id` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收集任务id',
  `collection_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收集名称',
  `collection_info` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '收集内容',
  `collection_start_time` datetime(0) NOT NULL COMMENT '开始时间',
  `collection_end_time` datetime(0) NOT NULL COMMENT '截止时间',
  `collection_items_amount` int(0) NOT NULL COMMENT '收集项数量',
  `class_id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收集对象班级id',
  `class_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收集对象班级名',
  PRIMARY KEY (`collection_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for collection_items
-- ----------------------------
DROP TABLE IF EXISTS `collection_items`;
CREATE TABLE `collection_items`  (
  `collection_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收集任务id',
  `index` int(0) NOT NULL COMMENT '收集项序号',
  `info` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述信息',
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '类型(问答,文件,选择等等)\r\n0[jpg,png,gif]\r\n1[请填写***]\r\n2[A选项,B选项,C选项]',
  PRIMARY KEY (`collection_id`, `index`) USING BTREE,
  INDEX `collection_id`(`collection_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for collection_record
-- ----------------------------
DROP TABLE IF EXISTS `collection_record`;
CREATE TABLE `collection_record`  (
  `collection_id` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收集任务id',
  `index` int(0) NOT NULL COMMENT '收集项的序号',
  `student_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '学生id',
  `student_name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `submit_time` datetime(0) NOT NULL COMMENT '提交时间',
  `submit_content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '提交内容',
  PRIMARY KEY (`collection_id`, `index`, `student_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;


-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户id',
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `password` varchar(110) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码（加密后）',
  `email` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱',
  `academy` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '所属学院',
  `identity` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '身份',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('994793770', 'super_admin', 'pbkdf2:sha256:260000$cRgVLLw3liQKvaKs$4edacc6ee6c805315ced4dc97ad748cc47114e1259295b59fa8d79cc68acc2b1', '994793770@qq.com', '', 'super_admin');
INSERT INTO `user` VALUES ('sk_admin', 'sk_admin', 'pbkdf2:sha256:260000$cRgVLLw3liQKvaKs$4edacc6ee6c805315ced4dc97ad748cc47114e1259295b59fa8d79cc68acc2b1', '994793770@qq.com', '数学与数据科学学院（软件学院）', 'admin');

-- ----------------------------
-- Table structure for user_n
-- ----------------------------
DROP TABLE IF EXISTS `user_n`;
CREATE TABLE `user_n`  (
  `id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户id',
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `password` varchar(110) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码（加密后）',
  `email` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱',
  `academy` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '学院',
  `identity` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '身份',
  `activate_code` varchar(110) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱激活码',
  `activate_permission` tinyint(1) NOT NULL COMMENT '是否得到管理员激活',
  PRIMARY KEY (`activate_code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_n
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
