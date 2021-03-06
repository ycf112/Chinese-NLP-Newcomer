## -1. 爬取政府工作报告：
### 利用教育网的便利爬取全国所有省市的政府工作报告，使用selenium驱动chrome在静默状态下获得网页html,使用BeautifulSoup获取文本内容，累计获取13000余份政府工作报告；

## -2. 对爬取数据进行处理：
### 在政府网站获取历年各省市行政编码，使用gb2260第三方lib库传入地区名对应的行政编码后，获得省市区三级行政名，对爬取的文件进行“年省市区.txt”重命名，爬取的统计结果使用pyecharts绘制3D柱状图和地形图，代码文件为pyecharts_plot.py；
![省级统计](https://github.com/xhlgogo/Chinese-NLP-Newcomer/blob/master/pyecharts_result/map.gif)
![年代统计](https://github.com/xhlgogo/Chinese-NLP-Newcomer/blob/master/pyecharts_result/3Dbar.gif)

## -3. 分词：
### 使用哈工大ltp的python封装：pyltp,分词任务为IO密集型，因此选择python多线程分词，代码文件为cut_pyltp.py；

## -4. lda：
### 使用gensim对537个省级政府工作报告进行lda文本主题分类，分类结果使用pyecharts绘制时间线散点图，代码文件为lda_model.py；
![lda主题关键词](https://github.com/xhlgogo/Chinese-NLP-Newcomer/blob/master/pyecharts_result/lda_timeline.gif)

## -5. k-means：
### 使用sklearn对537个省级政府工作报告进行k-means文本聚类，分类结果使用pyecharts二维散点图，代码文件为My_KMeans.py.
![k-means聚类结果](https://github.com/xhlgogo/Chinese-NLP-Newcomer/blob/master/pyecharts_result/k-means%E8%81%9A%E7%B1%BB.png)

## -6. 贝叶斯分类：
### 使用sklearn对537个省级政府工作报告进行多项式贝叶斯MultinomialNB和高斯贝叶斯GaussianNB分类：
#### 0）样本集为去除人名、地名、机构名的政府工作报告中，具有相同语法结构的句子，每个报告为一个样本，每个样本包含若干条重复两次以上的相同语法结构语句；
![相似句](https://github.com/xhlgogo/Chinese-NLP-Newcomer/blob/master/pyecharts_result/%E7%9B%B8%E4%BC%BC%E5%8F%A5.gif)
#### 1）每次训练随机按省市比例抽取样本3/4作为训练集，剩余1/4作为测试集；
#### 2）使用卡方分布chi2选取最佳文本特征数；
#### 3）结果表明：在742个特征时MultinomialNB在测试集上准确率能达到0.8378378378378378；在769个特征时GaussianNB在测试集上准确率能达到0.7297297297297297
#### 4）主函数见My_Bayes.py，工具函数见tools.py，
#### 5）不同卡方分布选择的特征数下的分类得分见文件“pyecharts_result\Multinomial(GaussianNB)_score_dict-去除人名地名机构名.json”

## -7. 基于gensim的doc2vec最佳文档嵌入模型分类：
### 期刊在投，不便展示，训练代码可见知乎专栏https://zhuanlan.zhihu.com/c_1069570763173982208
### 取最佳嵌入维度和滑动窗口训练得到的doc2vec文档向量，结合xgboost，3/4训练，1/4预测后分省市进行的分类结果统计。
![省域分类结果](https://github.com/xhlgogo/Chinese-NLP-Newcomer/blob/master/pyecharts_result/%E7%9C%81%E5%9F%9F%E5%88%86%E7%B1%BB%E7%BB%93%E6%9E%9C.png)
