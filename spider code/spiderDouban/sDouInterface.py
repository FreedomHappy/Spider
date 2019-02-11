#encoding: utf-8
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import test
import sqt
import sDoufun


class SWindow(QMainWindow,sqt.Ui_MainWindow):
	def __init__(self, parent=None):
		super(SWindow, self).__init__(parent)
		self.setupUi(self)
		self.Top250Bt.clicked.connect(self.getTop250)
		self.nowplayingBt.clicked.connect(self.getNowplaying)
		self.SingleBt.clicked.connect(self.SingleMovie)
		self.updateBt.clicked.connect(self.uplist)
		self.commentBt.clicked.connect(self.scomm)
		self.urlpool.itemDoubleClicked.connect(self.urlpool_click)
		self.movinfopool.itemDoubleClicked.connect(self.discomm)
		self.__init_urlpool()
		self.__init_movinfo()
		self.show()
		self.upooljudge=False
	def closeEvent(self, event):
		reply = QMessageBox.question(self, '确认', '确认退出吗', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()
	def SingleMovie(self):
		url=[str(self.urlLine.text())]
		sDoufun.insert_mSubject(url)
		if self.upooljudge==False:
			sDoufun.insert_urlpool(url)
		else:
			self.upooljudge=False
		QMessageBox.information(self,'电影爬取','电影爬取成功，并且URL已存！')
	def __init_urlpool(self):
		info=sDoufun.getUrlpoolInfo()
		for i in info:
			i='--'.join(i)
			newitem = QListWidgetItem()
			newitem.setText(i)
			self.urlpool.addItem(newitem)
	def __init_movinfo(self):
		minfo=sDoufun.getMovieinfo()
		for i in minfo:
			i='--'.join(i)
			newitem = QListWidgetItem()
			newitem.setText(i)
			self.movinfopool.addItem(newitem)
	def uplist(self):
		self.urlpool.clear()
		self.movinfopool.clear()
		self.__init_urlpool()
		self.__init_movinfo()
		QMessageBox.information(self,'更新提示','列表更新成功！')
	def urlpool_click(self):
		self.urlLine.clear()
		itemlist=self.urlpool.selectedItems() 
		get=itemlist[0].text()
		url=str(get).split('--')[0]
		self.urlLine.setText(url)
		self.upooljudge=True
	def getTop250(self):
		DouBanTop250_url='https://movie.douban.com/top250'
		urls=sDoufun.url_All(DouBanTop250_url)
		print(urls)
		impath="F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/Top250/"
		#sDoufun.insert_mSubject(urls,impath)
		#sDoufun.insert_urlpool(urls)
		QMessageBox.information(self,'电影爬取','电影Top250爬取成功，并且URL已存！')
	def getNowplaying(self):
		NowPlaying_FuZhou='https://movie.douban.com/cinema/nowplaying/fuzhou/'
		impath="F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/NowPlaying/"
		urls=sDoufun.nowPlaying(NowPlaying_FuZhou)
		sDoufun.insert_mSubject(urls,impath)
		sDoufun.insert_urlpool(urls)
		QMessageBox.information(self,'电影爬取','正在上映电影（福州）爬取成功，并且URL已存！')
	def scomm(self):
		itemlist=self.movinfopool.selectedItems() 
		if not itemlist:
			QMessageBox.warning(self,'评论爬取','没有选中电影！')
			return
		get=itemlist[0].text()
		movno=str(get).split('--')[0]
		sDoufun.mComment(movno)
		QMessageBox.information(self,'评论爬取','%s评论爬取成功!'%(movno))
	def discomm(self):
		self.commentpool.clear()
		itemlist=self.movinfopool.selectedItems() 
		get=itemlist[0].text()
		movno=str(get).split('--')[0]
		comm=sDoufun.dbcomment(movno)
		if comm==-1:
			newitem = QListWidgetItem()
			newitem.setText('此电影还未获取评论！')
			self.commentpool.addItem(newitem)
			return 
		num=1
		for i in comm:
			i='--'.join([str(num),i])
			newitem = QListWidgetItem()
			newitem.setText(i)
			self.commentpool.addItem(newitem)
			num=num+1
def main():
	app = QApplication(sys.argv)
	spider=SWindow()
	sys.exit(app.exec_())


if __name__=='__main__':
	main()
'''
遗留代码
(1)继承封装成类例子
class TestDialog(QtWidgets.QDialog,test.Ui_Dialog):  
	def __init__(self,parent=None):  
		super(TestDialog,self).__init__(parent)  
		self.setupUi(self)
app=QtWidgets.QApplication(sys.argv)  
dialog=TestDialog()  
dialog.show()  
app.exec_()
(2)创建对话框
app=QtWidgets.QApplication(sys.argv)
widget=QtWidgets.QWidget()
widget.resize(400,100)
widget.setWindowTitle("This is a demo for PyQt Widget.")
widget.show()
exit(app.exec_())
'''