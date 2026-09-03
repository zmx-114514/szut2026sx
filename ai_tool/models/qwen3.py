"""qwen3 = Qwen3-30B 非推理，最快，首字~0.4s（日常推荐）"""
MODEL_ID = "Qwen/Qwen3-30B-A3B-Instruct-2507"
# 关闭思考模式，保证输出干净、首字快
EXTRA_BODY = {"enable_thinking": False}
