import tkinter as tk
from tkinter import ttk, messagebox
import re

class EnhancedTextProcessorApp:
    def __init__(self, root):
        self.root = root
        root.title("增强版文本处理工具")
        root.geometry("680x600")
        
        # 输入区域
        input_frame = ttk.LabelFrame(root, text="输入文本", padding=(10, 5))
        input_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        self.input_text = tk.Text(input_frame, height=12, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # 控制面板
        control_frame = ttk.Frame(root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 行首删除设置
        self.n_chars = tk.IntVar(value=0)
        ttk.Label(control_frame, text="删除行首字符数：").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(control_frame, from_=0, to=100, width=5, textvariable=self.n_chars).grid(row=0, column=1, padx=5)
        
        # 正则表达式设置
        ttk.Label(control_frame, text="正则表达式：").grid(row=0, column=2, padx=(20,5), sticky=tk.E)
        self.regex_entry = ttk.Entry(control_frame, width=25)
        self.regex_entry.grid(row=0, column=3, sticky=tk.W)
        
        # 处理按钮
        ttk.Button(control_frame, text="处理文本", command=self.process_text).grid(row=0, column=4, padx=20)

        # 输出区域
        output_frame = ttk.LabelFrame(root, text="处理结果", padding=(10, 5))
        output_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        self.output_text = tk.Text(output_frame, height=12, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部按钮
        bottom_frame = ttk.Frame(root)
        bottom_frame.pack(pady=10)
        ttk.Button(bottom_frame, text="复制结果", command=self.copy_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="清空所有", command=self.clear_all).pack(side=tk.LEFT, padx=5)

    def process_text(self):
        """处理文本的核心逻辑"""
        try:
            # 获取输入内容
            input_content = self.input_text.get("1.0", tk.END).strip()
            if not input_content:
                messagebox.showwarning("警告", "请输入要处理的文本！")
                return
            
            # 获取处理参数
            n = self.n_chars.get()
            regex_pattern = self.regex_entry.get().strip()
            
            # 处理每一行
            processed_lines = []
            for line in input_content.split('\n'):
                # 删除所有星号
                line = line.replace('*', '')
                
                # 删除行首指定字符数
                if n > 0:
                    line = line[n:] if len(line) > n else ""
                
                # 应用正则表达式替换
                if regex_pattern:
                    try:
                        line = re.sub(regex_pattern, '', line)
                    except re.error as e:
                        messagebox.showerror("正则表达式错误", f"无效的正则表达式：\n{str(e)}")
                        return
                
                processed_lines.append(line)
            
            # 显示处理结果
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", '\n'.join(processed_lines))
            
        except Exception as e:
            messagebox.showerror("处理错误", f"发生未知错误：\n{str(e)}")

    def copy_result(self):
        """复制结果到剪贴板"""
        result = self.output_text.get("1.0", tk.END).strip()
        if not result:
            messagebox.showwarning("警告", "没有可复制的内容！")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        messagebox.showinfo("成功", "结果已复制到剪贴板！")

    def clear_all(self):
        """清空所有内容"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.n_chars.set(0)
        self.regex_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedTextProcessorApp(root)
    root.mainloop()
