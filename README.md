# Copy-- 智能文本转换工具

![软件截图](https://github.com/user3446358124/Copy--/blob/main/screenshots/main_ui.png)

一款基于正则表达式的智能文本转换工具，支持自定义规则集管理，实时文本转换和剪贴板集成。

## 主要功能 ✅

### 已实现功能

- **实时文本转换**左侧输入实时同步转换结果，支持正则表达式规则应用
- **可视化规则管理**
  - 创建/编辑多规则集（`.json`格式保存）
  - 双击编辑正则表达式模式/替换内容
  - 规则启用状态即时切换
  - 智能规则排序（支持拖拽或按钮调整优先级）
- **智能编码处理**自动检测文件编码（支持UTF-8/GBK/GB2312）
- **用户友好设计**
  - 搜索结果高亮显示
  - 自动保存修改记录
  - 错误操作撤销/重做

### 未来计划 🚀

1. **系统集成增强**

   - 开机自启动（通过注册表/启动目录实现）
   - 状态栏托盘图标（最小化到系统托盘）
   - 剪贴板监听模式（后台静默运行）
2. **智能剪贴板处理**

   - 根据来源应用自动匹配规则（如：从Excel复制时应用表格清洗规则）
   - 直接修改剪贴板内容（无需手动粘贴）
   - 多剪贴板历史支持（`Win+V`模式集成）
3. **OCR图文识别**

   - 截图自动识别文字（集成Tesseract OCR引擎）
   - 图片拖拽识别区域选择
   - 多语言文本识别支持（中/英/日/韩）

## 安装与使用 🛠️

### 环境要求

```
chardet==5.2.0        
pillow==10.3.0        
pyinstaller==6.13.0   

# OCR相关（未来功能）
pytesseract==0.3.10   
openai-whisper==20231117  

# 高级剪贴板功能
pyperclip==1.8.2      
pywin32==306           
```

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/user3446358124/Copy--.git

# 运行程序
python Main.py
```

### 自用规则集

```json
[
  {
    "enabled": true,
    "pattern": "\\\\\\[",
    "replacement": "$$",
    "comment": "将转义左方括号转换为数学公式块开始符"
  },
  {
    "enabled": true,
    "pattern": "\\\\\\]",
    "replacement": "$$",
    "comment": "将转义右方括号转换为数学公式块结束符"
  },
  {
    "enabled": true,
    "pattern": "\\\\\\(",
    "replacement": "$",
    "comment": "将转义左圆括号转换为行内公式开始符"
  },
  {
    "enabled": true,
    "pattern": "\\\\\\)",
    "replacement": "$",
    "comment": "将转义右圆括号转换为行内公式结束符"
  },
  {
    "enabled": true,
    "pattern": "\\\\\\{",
    "replacement": "{",
    "comment": "修复转义左大括号"
  },
  {
    "enabled": true,
    "pattern": "\\\\\\}",
    "replacement": "}",
    "comment": "修复转义右大括号"
  },
  {
    "enabled": true,
    "pattern": "\\\\\\|",
    "replacement": "|",
    "comment": "修复转义竖线符号"
  },
  {
    "enabled": true,
    "pattern": "\\\\([^\\[\\](){}|])",
    "replacement": "\\1",
    "comment": "移除不必要的单反斜杠转义"
  },
  {
    "enabled": true,
    "pattern": "\\$\\$(.*?)\\$\\$",
    "replacement": "\n$$$1$$\n",
    "comment": "格式化数学公式块间距"
  }
]
```

