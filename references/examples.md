> 公开发布版说明：本包仅保留三套无声样例与画面源码，原音轨、第三方原片、被否定历史和生产验证报告不随包发布

# 专门的样例库

examples/index.html是可直接打开的本地样例页，catalog.json记录分类与历史。

目录：candidates/<id>为待选；approved/<id>-v1为用户认可后的版本；rejected分类保留否定记录，避免重用。每个样例包含preview.mp4、poster.png、可播放HTML、scenes.js、film/timeline、字体/声音、本片文稿、sample.json七项来源与采用记录。

`python scripts/samples.py gallery`打开样例页。它只浏览本地文件；不代表七包可以缺失后继续制作。

`samples.py add <项目> --id <小写ID> --title <标题> --category <故事/对象接续/运镜等> --description <用途>`要求实际MP4和七项贡献检查通过，默认存本技能examples；不会把空目录或仅图片当完成样例。

`samples.py approve <id> --evidence <用户真实认可依据>`保留待选副本、复制到approved版本并记录。`reject`记录否定与原因。工具只记证据，不判断是否真实；沉默、自评、技术测试不能当认可。

入库不自动锁定风格。认可后再style-lock/export-style保存对应风格包；没有认可条目时需要先展示短样。历史旧片没有重新获认可，不因导入而成为默认模板。

样例页可双击打开，里面的MP4可直接看；HTML源码工程需本地HTTP服务，使用对应tools/studio.py serve。发布给别人前保留素材许可，私有配置和外部未授权素材不随包分发。

用户提供的三条原片保存在examples/references/ref-1、ref-2、ref-3；examples/compare.html并排播放原片与新24秒候选，附analysis.md和来源记录。原片是参考材料，不是本技能生成结果。
