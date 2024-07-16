## 介绍
此脚本的作用是，作用是叫 epub 格式的文件，转为通过阿里的 cosyvoice-v1 模型转换为音频。

## 使用方式
- 需要到阿里申请api key，具体方式可以进行Google搜索查到，在此不做赘述；
- 在工作目录下（ai-toolkit-script）下创建.env 文件，并在文件中创建写入申请的api-kiy格式为：`API_KEY="sk-2b71b680ac2"`
- 更改chat-tts.py 文件中的目标目录`epub_path,base_output_folder,audio_output_folder`
- 加载项目依赖项，在终端执行命令：`pip3 install -r requirements.txt`

## 改进
- [ ] 目前生成的音频文件是相对独立的，无法进行连续的播放，可以给一个简单的web端或用户端做连续播放处理体验将会更好
- [ ] 当前的音频生成是单线程的，效率有些低。可以做进一步的并发处理
- [ ] 当前的音色是在代码中些死的，可以优化为动态配置会更有好点
- [ ] 目标`epub_path,base_output_folder,audio_output_folder` 都可应该作为可配置项，与前端接口做对接