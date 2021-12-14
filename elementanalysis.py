import re
import requests,bs4
from requests.auth import HTTPBasicAuth


#这个类的作用：
# 解析元素和提取元素
# 包括过滤好完整的数据传给其他模块使用
class Elementanalysis():
    def __init__(self,url):
        # url = ("http://jira.intretech.com:8080/browse/" + jiraid)
        res = requests.get(url, auth=HTTPBasicAuth('10324', '123aaa'))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        self.soup=soup

    # 问题详情-类型
    def type_val(self):
        try:
            type_check = self.soup.find(id="type-val")
            type_check_value = type_check.text.strip()
            return type_check_value
        except AttributeError:
            # print("找不到问题类型，出现以下异常%s" % AttributeError)
            return False

    #问题详情-状态
    def bug_status(self):
        try:
            bug_status = self.soup.find(id="status-val")  # 问题详情中的状态
            bug_status_text = bug_status.text.strip()
            # print(bug_status_text)
            return bug_status_text
        except AttributeError:
            # print("找不到问题状态，出现以下异常%s" % AttributeError)
            return False

    #问题详情-解决结果
    def bug_status_type(self):
        try:
            bug_status_type = self.soup.find(id="resolution-val")  # 问题详情中的类型
            bug_status_type_text = bug_status_type.text.strip()
            # print(bug_status_type_text)
            return bug_status_type_text
        except AttributeError:
            # print("找不到问题详情中断饿解决结果，出现以下异常%s" % AttributeError)
            return False

    #问题详情-影响版本
    def versions_val(self):
        try:
            versions = self.soup.find(id="versions-val")
            versions_text = versions.text.strip()
            return versions_text
        except AttributeError:
            return False

    #问题详情-修复版本
    def fixfor_val(self):
        try:
            # 如果没有写版本号，返回的结果是“无”，不是False
            fixfor = self.soup.find(id="fixfor-val")
            fixfor_text = fixfor.text.strip()
            return fixfor_text
        except AttributeError:
            return False

    #问题详情-模块
    def components(self):
        try:
            components = self.soup.find(id="components-field")  # 问题详情中的“模块”---输出的结果有点话都有值
            components_text = components.text.strip()
            # print(components_text)
            return components_text
        except AttributeError:
            # print("找不到模块，出现以下异常%s" % AttributeError)
            return False

    # 问题详情-发生概率
    def probability_of_occurrence(self):
        try:
            faxian = self.soup.find(id="customfield_11350-val")
            # print(faxian.text)
            # print(faxian.text.strip())  #TODO 为什么faxian.text.strip的结果会多出None？，虽然提取的内容现在不做判断，但是多个None要分析下为啥
            return faxian.text.strip()
        except AttributeError:
            # print("无“发生概率”，出现以下异常%s" % AttributeError)
            return False

    # 问题详情-前提条件
    def premise_condition(self):
        try:
            qianti = self.soup.find(id="customfield_11358-val")
            # print(qianti.text.strip())
            return qianti.text.strip()
        except AttributeError:
            # print("无“前提条件”，出现以下异常%s" % AttributeError)
            return False
    # 问题详情-操作步骤
    def steps(self):
        try:
            caozuo = self.soup.find(id="customfield_11359-val")
            # print(caozuo.text.strip())
            return caozuo.text.strip()
        except AttributeError:
            # print("无“操作步骤”，出现以下异常%s" % AttributeError)
            return False
    # 问题详情-实际结果
    def actual_results(self):
        try:
            shiji = self.soup.find(id="customfield_11360-val")
            # print(shiji.text.strip())
            return shiji.text.strip()
        except AttributeError:
            # print("无“实际结果”，出现以下异常%s" % AttributeError)
            return False
    # 问题详情-预期结果
    def expected_results(self):
        try:
            yuqi = self.soup.find(id="customfield_11361-val")
            # print(yuqi.text.strip())
            return yuqi.text.strip()
        except AttributeError:
            # print("无“预期结果”，出现以下异常%s" % AttributeError)
            return False

    # 问题详情-影响范围
    def scope_of_influence(self):
        try:
            yingxinag = self.soup.find(id="customfield_11362-val")
            # print(yingxinag.text.strip())
            return yingxinag.text.strip()
        except AttributeError:
            # print("无“影响范围”，出现以下异常%s" % AttributeError)
            return False
    # 问题详情-是否提交代码
    def submit_code(self):
        try:
            tijiao = self.soup.find(id="customfield_11363-val")
            # print(tijiao.text.strip())
            return tijiao.text.strip()
        except AttributeError:
            # print("无“是否提交代码”，出现以下异常%s" % AttributeError)
            return False
    # 问题详情-原因分析
    def cause_analysis(self):
        try:
            yuanyin = self.soup.find(id="customfield_10754-val")
            # print(yuanyin.text.strip())
            return yuanyin.text.strip()
        except AttributeError:
            # print("无“原因分析”，出现以下异常%s" % AttributeError)
            return False
    # 问题详情-解决措施
    def solution(self):
        try:
            jiejue = self.soup.find(id="customfield_10040-val")
            # print(jiejue.text.strip())
            return jiejue.text.strip()
        except AttributeError:
            # print("无“解决措施”，出现以下异常%s" % AttributeError)
            return False

    # 提取描述内容
    def description(self):
        try:
            get_miaoshu = self.soup.find(id="descriptionmodule")
            miaoshu = get_miaoshu.text.strip()
            return miaoshu
        except AttributeError:
            # print("无“描述”，出现以下异常%s" % AttributeError)
            return False

    # 附件有无判断
    # 附件只要判断能提取到这个id就可以，对于文件内容不做判断,如果没有附件会返回None
    def attachment(self):
        try:
            fujian = self.soup.find(id="attachmentmodule")
            # print(fujian)
            if fujian == None:
                return False
            else:
                return True
        except AttributeError:
            # print("无“解决措施”，出现以下异常%s" % AttributeError)
            return False

    #提取 活动中所有的项对应的链接
    def activity_link(self):
        try:
            huodong = self.soup.find(id="issue-tabs")
            # print(huodong)
            # print(type(huodong))
            # print(huodong.text.strip())
            # 活动下对应的内容，名称-链接，用字典来表示
            huodong_tiqu = huodong.find_all("li")
            # print(len(huodong_tiqu))
            # print(huodong_tiqu[0].get("data-label"))
            activity_link_dict = {}
            for item in huodong_tiqu:
                huodong_key = item.get("data-label")
                # print(huodong_key)
                huodong_keyvalue = item.get("data-href")
                # print(huodong_keyvalue)
                activity_link_dict.update({huodong_key:huodong_keyvalue})
                # print(activity_link_dict)
                # print(activity_link_dict['所有'])
            return activity_link_dict
        except AttributeError:
            # print("无“活动-链接”，出现以下异常%s" % AttributeError)
            return False

    # 提取 活动-备注中的内容
    def comment(self):
        try:
            neirong_mignzi = self.soup.find_all("div", attrs={"class", "action-details"})
            # print(neirong_mignzi)
            # print(len(neirong_mignzi))
            # print(neirong_mignzi.text.strip())  #find_all 需要循环才能打出来，不然会报错
            match_flag = 0
            beizhu_neirong = ''
            for i in neirong_mignzi:
                # 备注里面主要找有备注可以关闭的字眼就好，不用判断谁写的
                mingzi = i.find_all("a")
                beizhu = i.text.strip()
                # print(beizhu)
                #备注内容按照时间顺序倒序排列，最新的排最前
                beizhu_neirong += beizhu
            return beizhu_neirong
                # 备注里面的内容
                #ZMLY-260：需求如此，不更改    -->  .*不.*改
                #ZMLY-218:经过确认，需求已更改，默认不打勾 --> 经.*
                #ZMLY-204：该问题在安卓V1.0.2版本出现另外一种现象，见xxxx  -- > .*重复.*见.*
            #     comment_match = ".*关闭|验证通过|关闭.*问题|已解决|已修复|未.*现|重复创建|已.*建|.*暂时.*"
            #     comment = re.findall(comment_match, beizhu)
            #     if len(comment) != 0:
            #         match_flag = 1
            # if match_flag == 1:
            #     return True
            # else:
            #     return False

        except AttributeError:
            print("无“备注”，出现以下异常%s" % AttributeError)
            return False

    #提取 活动-所有中的“创建问题”   这条要重新get url进行解析获取内容
    def activities_all(self):
        try:
            huodong_suoyou = self.soup.find_all("div", attrs={"class", "action-details"})
            # print(huodong_suoyou)
            for i in huodong_suoyou:
                # print(i)
                get_num = i.find("a")
                neirong = i.text.strip()
                match_str = "创建了问题"
                match = re.findall(match_str, str(neirong))
                if len(match) != 0:
                    creater = get_num.get("rel")
                    # print(creater)  #结果是一个数组
                    return creater[0]
                else:
                    return False
        except AttributeError:
            # print("无“活动 - 所有 ：第一次创建”，出现以下异常%s" % AttributeError)
            return False

    #经办人
    def assignee(self):
        try:
            assignee = self.soup.find_all("span", attrs={"class", "user-hover"})
            assignee_gonghao = assignee[0].get('rel')  # 经办人工号
            # print(assignee_gonghao, reporter_gonghao)
            return assignee_gonghao
        except AttributeError and IndexError:
            #问题不存在的时候，会报数组超过范围值的异常
            # print("找不到经办人，出现以下异常%s" % AttributeError)
            return False

    # 报告人
    def reporter(self):
        try:
            reporter = self.soup.find_all("span", attrs={"class", "user-hover"})
            reporter_gonghao = reporter[1].get('rel')  # 报告人工号
            # print(assignee_gonghao, reporter_gonghao)
            return reporter_gonghao
        except AttributeError and IndexError:
            #问题不存在的时候，会报数组超过范围值的异常
            # print("找不到报告人，出现以下异常%s" % AttributeError)
            return False


    #创建时间
    def creat_date(self):
        try:
            creat_date = self.soup.find(id="create-date")
            creat_time = creat_date.find("time", attrs={"class", "livestamp"})
            creattime = creat_time.get("datetime")
            return creattime
        except AttributeError:
            # print("找不到创建时间，出现以下异常%s" % AttributeError)
            return False

    #解决时间
    def resolved_date(self):
        try:
            resolved_date = self.soup.find(id="resolved-date")
            resolved_time = resolved_date.find("time", attrs={"class", "livestamp"})
            resolvedtime = resolved_time.get("datetime")
            return resolvedtime
        except AttributeError:
            # print("找不到解决时间，出现以下异常%s" % AttributeError)
            return False

    #问题不存在   如果问题存在，会提取问题的标题;如果问题不存在，输出结果为“问题不存在”,不会输出False
    def issuecontent(self):
        try:
            issuecontent = self.soup.find("div", attrs={"class", "aui-page-header-main"})
            issue_content = issuecontent.text
            return issue_content
        except AttributeError:
            # print("找不到'问题不存在'%s" % AttributeError)
            return False

    #问题-主题
    def summary(self):
        try:
            summary_val = self.soup.find(id="summary-val")
            summary_val = summary_val.text.strip()
            # print(summary_val)
            return summary_val
        except AttributeError:
            return False




    #提取父链接id
    def parent_issue(self):  #如果有的话可能要在这里做处理判断父连接
        try:
            parent_issue=self.soup.find(id="parent_issue_summary")
            # print(parent_issue)
            parent_issue_id = parent_issue.get("data-issue-key")
            # print(parent_issue_id)
            #打印问题标题
            # parent_bug_title = self.soup.title.string
            # print(parent_bug_title)

            #这些不应该放在这里，应该放在type_check里去判断，type_check是用来判断类型的，父问题类型和子问题类型都应该判断
            # match_str = "Buglist|buglist|问题集"
            # match = re.findall(match_str, str(parent_bug_title.text))
            # print("match长度" %len(match))
            # parent_issue_isbug =False
            # if len(match) != 0:
            #     print("子任务的父问题是buglist")
            #     parent_issue_isbug = True
            # return parent_issue_id,parent_issue_isbug
            return parent_issue_id

        except AttributeError:
            # print("找不到父链接，出现以下异常%s" % AttributeError)
            return False

    #判断父链接是否为buglist
    def parent_type_check(self):
        try:
            type_check = self.soup.find(id="type-val")
            type_check_value = type_check.text.strip()
            print(type_check_value)
            if type_check_value == "问题点":
                return True
            else:
                parent_bug_title = self.soup.title.string
                print(parent_bug_title)
                match_str = "Buglist|buglist|问题集"
                match = re.findall(match_str, str(parent_bug_title))
                print(len(match))
                if len(match):
                    return True
                else:
                    return False
        except AttributeError:
            # print("找不到问题类型，出现以下异常%s" % AttributeError)
            return False
    #  问题类型  直接在里面判断类型好了








#以下为调试用，不要删除
# url='http://jira.intretech.com:8080/browse/GGXB-4800'
# res=requests.get(url,auth=HTTPBasicAuth('10324','123aaa'))
#
# res.raise_for_status()
#
# soup=bs4.BeautifulSoup(res.text,features="html.parser")

# GGXB-4253   GGXB-5315?page=com.atlassian.jira.plugin.system.issuetabpanels:all-tabpanel
# e=Elementanalysis('http://jira.intretech.com:8080/browse/ZMLY-1470')  #GGXB-5314


# '''
# print(e.type_val())
# print(e.bug_status())
# print(e.bug_status_type())
# print(e.components())
# #bug 描述
# print(e.probability_of_occurrence())
# print(e.premise_condition())
# print(e.steps())
# print(e.actual_results())
# print(e.expected_results())
# #
# print(e.description())
#
# #开发解决填写
# print(e.cause_analysis())
# print(e.scope_of_influence())
# print(e.solution())
# print(e.submit_code())

##
# print(e.issuecontent())
# print(e.resolved_date())
# print(e.creat_date())
# print(e.assignee())
# print(e.reporter())

# print(e.activity_link())
# print(e.activities_all())
# print(e.comment())
# print(e.description())
# print(e.attachment())
#
# print(e.parent_issue())
# print(e.summary())

# '''
