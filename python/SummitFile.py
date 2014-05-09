# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import os.path
import shutil
import hashlib
import binascii
import win32api
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getFileVersion(file_name):
	info = win32api.GetFileVersionInfo(file_name, os.sep)
	ms = info['FileVersionMS']
	ls = info['FileVersionLS']
	version = '%d.%d.%d.%d' %(win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
	return version
def copyReleaseFile(file_name, dest_path):
	file_version = getFileVersion(file_name)
	created_path = os.path.join(dest_path, file_version)
	if os.path.exists(created_path):
		return False, 'have the same file path!'
	os.mkdir(os.path.join(dest_path, file_version))
	shutil.copy(file_name, created_path)
	return True, created_path + file_name[file_name.rfind('\\'): len(file_name)]
def createInfoFile(src_path, info_name):
	created_path = src_path[0: src_path.rfind('\\') + 1]
	desc_info_path = os.path.join(created_path, info_name)
	print 'desc_info_path: %s' % desc_info_path
	h_md5 = hashlib.md5()
	h_sha1 = hashlib.sha1()
	f_src_file = open(src_path, 'rb')
	all_file_contents = ''
	for line in f_src_file:
		h_md5.update(line)
		h_sha1.update(line)
		all_file_contents += line
	f_info_file = open(desc_info_path, 'w')
	info_contents = u'%s\n大小：%u字节\n文件版本：%s\n修改时间：%s\nMD5：%s\nSHA1：%s\nCRC32：%X' % \
					( \
						src_path[src_path.rfind('\\') + 1: len(src_path)], \
						os.path.getsize(src_path), \
						getFileVersion(src_path), \
						time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.localtime(os.path.getmtime(src_path))), \
						h_md5.hexdigest(), \
						h_sha1.hexdigest(), \
						(binascii.crc32(all_file_contents) & 0xffffffff) \
					)
	f_info_file.write(info_contents)
	f_src_file.close()
	f_info_file.close()
def summitFile(file_path, dest_path):
	ret = copyReleaseFile(file_path, dest_path)
	if (ret[0] == True):
		createInfoFile(ret[1], u'file_info.txt')
		return True
	return False
def svnAddFile(svn_path, new_path_name):
	os.chdir(svn_path)
	command = 'svn add %s' % new_path_name
	os.system(command)
def svnSummit(svn_path, message):
	os.chdir(svn_path)
	command = 'svn commit -m "%s"' % message
	os.system(command)

choice = raw_input('please input the choice:\n1:提交收藏夹\n2:提交广告弹窗\n3:提交桌面图标\n'.decode('utf8').encode('gbk'))
message = raw_input(u'please input the summit message:\n'.decode('utf8').encode('gbk'))

#收藏夹
if (choice == '1'): 
	#提交主程序
	main_file_path = unicode('D:\\work\\laughing_project\\collect_dir\\Release\\collect_dir.dll', 'utf8')
	dest_path = unicode('D:\\work\\测试部提交svn\\收藏夹\\tpsp版本\\生成图标', 'utf8')
	file_info_message = ''
	if (summitFile(main_file_path, dest_path)):
		file_info_message += 'main file: %s;' % getFileVersion(main_file_path)
		svnAddFile(unicode('D:\\work\\测试部提交svn\\收藏夹\\tpsp版本\\生成图标', 'utf8'), getFileVersion(main_file_path))
	#提交32位保护dll
	help_32bits_file_path = unicode('D:\\work\\laughing_project\\collect_dir\\Release\\EyooiSechelper_x32.dll')
	dest_path = unicode('D:\\work\\测试部提交svn\\收藏夹\\tpsp版本\\保护dll_x32', 'utf8')
	if (summitFile(help_32bits_file_path, dest_path)):
		file_info_message += 'main file: %s;' % getFileVersion(help_32bits_file_path)
		svnAddFile(unicode('D:\\work\\测试部提交svn\\收藏夹\\tpsp版本\\保护dll_x32', 'utf8'), getFileVersion(help_32bits_file_path))
	#提交64位保护dll
	help_64bits_file_path = unicode('D:\\work\\laughing_project\\collect_dir\\x64\Release\\EyooiSechelper_x64.dll')
	dest_path = unicode('D:\\work\\测试部提交svn\\收藏夹\\tpsp版本\\保护dll_x64', 'utf8')
	if (summitFile(help_64bits_file_path, dest_path)):
		file_info_message += 'main file: %s;' % getFileVersion(help_64bits_file_path)
		svnAddFile(unicode('D:\\work\\测试部提交svn\\收藏夹\\tpsp版本\\保护dll_x64', 'utf8'), getFileVersion(help_64bits_file_path))
	message = file_info_message + message
	if (file_info_message != '')
		svnSummit(unicode('D:\\work\\测试部提交svn\\收藏夹\\tpsp版本', 'utf8'), message)
#广告弹窗
elif (choice == '2'): 
	#提交主程序
	main_file_path = unicode('D:\\work\\laughing_project\\广告弹窗-v1.1.0.57\\Release\\AdPopup.dll', 'utf8')
	dest_path = unicode('D:\\work\\测试部提交svn\\广告弹窗\\tpsp版本\\主程序', 'utf8')
	file_info_message = ''
	if (summitFile(main_file_path, dest_path)):
		file_info_message += 'main file: %s;' % getFileVersion(main_file_path)
		svnAddFile(unicode('D:\\work\\测试部提交svn\\广告弹窗\\tpsp版本\\主程序', 'utf8'), getFileVersion(main_file_path))
	#提交32位bho
	bho_32bits_file_path = unicode('D:\\work\\laughing_project\\广告弹窗-v1.1.0.57\\Release\\BHO_GetUrl.dll')
	dest_path = unicode('D:\\work\\测试部提交svn\\广告弹窗\\tpsp版本\\网址弹窗bho_x32', 'utf8')
	if (summitFile(bho_32bits_file_path, dest_path)):
		file_info_message += '32bits BHO: %s;' % getFileVersion(bho_32bits_file_path)
		svnAddFile(unicode('D:\\work\\测试部提交svn\\广告弹窗\\tpsp版本\\网址弹窗bho_x32', 'utf8'), getFileVersion(bho_32bits_file_path))
	#提交64位bho
	bho_64bits_file_path = unicode('D:\\work\\laughing_project\\广告弹窗-v1.1.0.57\\x64\Release\\BHO_GetUrl_x64.dll')
	dest_path = unicode('D:\\work\\测试部提交svn\\广告弹窗\\tpsp版本\\网址弹窗bho_x64', 'utf8')
	if (summitFile(bho_64bits_file_path, dest_path)):
		file_info_message += '64bits BHO: %s;' % getFileVersion(bho_64bits_file_path)
		svnAddFile(unicode('D:\\work\\测试部提交svn\\广告弹窗\\tpsp版本\\网址弹窗bho_x64', 'utf8'), getFileVersion(bho_64bits_file_path))
	message = file_info_message + message
	if (file_info_message != '')
		svnSummit(unicode('D:\\work\\测试部提交svn\\广告弹窗\\tpsp版本', 'utf8'), message)

#桌面图标
elif (choice == '3'):
	#提交主程序
	main_file_path = unicode('D:\\work\\laughing_project\\桌面图标插件-V0.1.2.15\\Release\\desktop_icon.dll', 'utf8')
	dest_path = unicode('D:\\work\\测试部提交svn\\桌面图标\\tpsp版本', 'utf8')
	file_info_message = ''
	if (summitFile(main_file_path, dest_path)):
		file_info_message += 'main file: %s;' % getFileVersion(main_file_path)
		svnAddFile(unicode('D:\\work\\测试部提交svn\\桌面图标\\tpsp版本\\主程序', 'utf8'), getFileVersion(main_file_path))
	message = file_info_message + message
	if (file_info_message != '')
		svnSummit(unicode('D:\\work\\测试部提交svn\\桌面图标\\tpsp版本', 'utf8'), message)
else:
	None
raw_input('Enter!')
