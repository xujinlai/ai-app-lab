from prompt import DEFAULT_PLANNING_PROMPT, DEFAULT_SUMMARY_PROMPT

import os
from openai import OpenAI
from utils import get_current_date
import lunary



client = OpenAI(
    # 从环境变量中读取您的方舟API Key
    api_key=os.environ.get("ARK_API_KEY"), 
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 深度推理模型耗费时间会较长，建议您设置一个较长的超时时间，推荐为30分钟
    timeout=1800,
    )

lunary.monitor(client)

thread = lunary.open_thread()

prompt = lunary.render_template("deep-research-s1", {
    "max_search_words": 3,
    "meta_info": f"当前时间：{get_current_date()}",
    "question": "帮我查一下2024年11月上市的智能手机的价格，并给出一篇有关其中最便宜的一款的网络评测",
})

run_id = thread.track_message(prompt["messages"][0])

prompt["model"] = "deepseek-r1-250120"
print(f"#### prompt: {prompt}")
response = client.chat.completions.create(
    **prompt
)

if hasattr(response.choices[0].message, 'reasoning_content'):
    print(response.choices[0].message.reasoning_content)
print(response.choices[0].message.content)

run_id = thread.track_message(response.choices[0].message.to_dict())

lunary.track_feedback(run_id, {"thumb": "up"})