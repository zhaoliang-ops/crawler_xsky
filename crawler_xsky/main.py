# This is a sample Python script.


import json

import requests

# def get_cookies():
#     url = 'https://xskydata.jobs.feishu.cn/api/v1/config/job/filters/6'
#     resp = requests.get(url)
#     for k, v in resp.cookies.items():
#         print(k + "=" + v)

def send_requests(curPage, list_post):
    # 首页地址
    url = 'https://xskydata.jobs.feishu.cn/api/v1/search/job/posts'
    headers = {
        'Origin': 'https://xskydata.jobs.feishu.cn',
        "Content-Type": "application/json",
        'Referer': 'https://xskydata.jobs.feishu.cn/school',
        'authority': 'xskydata.jobs.feishu.cn',
        'x-csrf-token': 'njy0U0G1JJXo417EJpCxkAowp0ordciVJJbxjcVOwDA=',
        'website-path': 'school',
        'cookie': 'atsx-portal-session-v1=; channel=saas-career; platform=pc; '
                  's_v_web_id=verify_l06dm9gp_KeafgiBE_r9gg_4FYc_9OpG_CaFBDJErJNoI; device-id=7069658381104170510; '
                  'tea_uid=undefined; atsx-portal-session-v1=; atsx-portal-user-source-v1=; '
                  'SLARDAR_WEB_ID=38f84b4f-7b40-4ee0-a5be-b42a9afb60cc; '
                  'atsx-csrf-token=njy0U0G1JJXo417EJpCxkAowp0ordciVJJbxjcVOwDA%3D'}
    data = {"job_category_id_list": [], "keyword": "", "limit": 10, "location_code_list": [], "offset": curPage * 10,
            "portal_entrance": 1, "portal_type": 6, "recruitment_id_list": [], "subject_id_list": []}

    payload = json.dumps(data)

    # 发起网络请求，获取到返回的html

    response = requests.post(url=url, data=payload, headers=headers)
    if response.status_code == 405:
        return list_post
    res_json = json.loads(response.text)
    # print(res_json['data']['count'])
    count = res_json['data']['count']
    totalPageNum = int((count + 9) / 10)
    # print(totalPageNum)
    job_post_list = res_json['data']['job_post_list']
    for cur in job_post_list:
        # print('职位名称:' + cur['title'] + '--职位类别:' + cur['job_category']['name'] + '--工作地点:' + cur['city_info']['name'])
        list_post.append(cur['title'] + '|' + cur['job_category']['name'] + '|' + cur['city_info']['name'])
    curPage = curPage + 1
    if curPage < totalPageNum:
        send_requests(curPage, list_post)
    else:
        return list_post


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # cookies = get_cookies()
    curPage = 0
    list_post = []
    result = send_requests(curPage, list_post)
    if len(list_post) == 0:
        print("cookie-token过期")
        exit()
    # 7、爬取数据保存到文件
    json_file_path = 'school_post_data.json'
    json_file = open(json_file_path, mode='w')

    save_json_content = []
    for cur in list_post:
        split = str(cur).split('|')
        result_json = {
            "职位名称": split[0],
            "职位类别": split[1],
            "工作地点": split[2]}
        save_json_content.append(result_json)
    print(save_json_content)
    # json.dump(save_json_content, json_file, indent=4)
    json.dump(save_json_content, json_file, ensure_ascii=False, indent=4)  # 保存中文
