import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import re
import chardet  # 新增编码检测库

DEFAULT_RULESET = "default_rules.json"

class Rule:
    def __init__(self, enabled=True, pattern='', replacement='', comment=''):
        self.enabled = enabled
        self.pattern = pattern
        self.replacement = replacement
        self.comment = comment



import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import re
import chardet  # 新增编码检测库

DEFAULT_RULESET = "default_rules.json"

class RuleSetManager:
    def __init__(self):
        self.current_file = None
        self.rules = []
        self.ruleset_dir = "rulesets"
        os.makedirs(self.ruleset_dir, exist_ok=True)
        
        # 初始化默认规则集
        self.default_ruleset_path = os.path.join(self.ruleset_dir, DEFAULT_RULESET)
        self.init_default_ruleset()
        self.load_default_ruleset()

    def safe_json_load(self, file_path):
        """安全加载JSON文件，自动检测编码"""
        try:
            # 第一次尝试UTF-8
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except UnicodeDecodeError:
            # 检测实际编码
            with open(file_path, 'rb') as f:
                rawdata = f.read()
                encoding = chardet.detect(rawdata)['encoding']
            
            try:
                # 使用检测到的编码再次尝试
                with open(file_path, 'r', encoding=encoding) as f:
                    return json.load(f)
            except Exception as e:
                # 如果仍然失败，尝试常见编码
                for codec in ['gbk', 'gb2312', 'big5', 'utf-16']:
                    try:
                        with open(file_path, 'r', encoding=codec) as f:
                            return json.load(f)
                    except:
                        continue
                raise ValueError(f"无法解码文件: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON格式错误: {str(e)}")

    def init_default_ruleset(self):
        """创建/修复默认规则集"""
        if not os.path.exists(self.default_ruleset_path):
            self._create_new_default_ruleset()
        else:
            try:
                # 验证文件完整性
                self.safe_json_load(self.default_ruleset_path)
            except Exception as e:
                os.remove(self.default_ruleset_path)
                self._create_new_default_ruleset()

    def _create_new_default_ruleset(self):
        """创建新的默认规则集"""
        default_rules = [
            {
                "enabled": True,
                "pattern": r"\\\[",
                "replacement": "[",
                "comment": "转义左方括号"
            },
            {
                "enabled": True,
                "pattern": r"\\\]",
                "replacement": "]",
                "comment": "转义右方括号"
            }
        ]
        try:
            with open(self.default_ruleset_path, 'w', encoding='utf-8') as f:
                json.dump(default_rules, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("错误", f"创建默认规则集失败: {e}")

    def load_default_ruleset(self):
        """加载默认规则集"""
        try:
            data = self.safe_json_load(self.default_ruleset_path)
            self.rules = [Rule(**item) for item in data]
            self.current_file = self.default_ruleset_path
        except Exception as e:
            messagebox.showerror("错误", f"加载默认规则集失败: {e}")

    def save_to_file(self, path, rules):
        """保存规则到文件"""
        data = [rule.__dict__ for rule in rules]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def apply_rules(self, text):
        """应用当前规则集"""
        for rule in self.rules:
            if rule.enabled:
                try:
                    text = re.sub(r'{}'.format(rule.pattern), rule.replacement, text)
                except Exception as e:
                    print(f"规则应用错误: {e}")
        return text

class RuleEditor(tk.Toplevel):
    def __init__(self, master, ruleset_manager):
        super().__init__(master)
        self.ruleset_manager = ruleset_manager
        self.title("规则编辑器")
        self.geometry("1000x600")
        self.editing = False  # 跟踪编辑状态
        
        # 搜索框
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5, fill=tk.X)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="搜索", command=self.filter_rules).pack(side=tk.LEFT)
        
        # 规则表格
        self.tree = ttk.Treeview(self, columns=('enabled', 'pattern', 'replacement', 'comment'), show='headings')
        self.tree.heading('enabled', text='启用', anchor='center')
        self.tree.column('enabled', width=50, anchor='center')
        self.tree.heading('pattern', text='正则表达式')
        self.tree.column('pattern', width=300)
        self.tree.heading('replacement', text='替换内容')
        self.tree.column('replacement', width=200)
        self.tree.heading('comment', text='注释')
        self.tree.column('comment', width=400)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<ButtonRelease-1>', self.on_single_click)
        
        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="添加规则", command=self.add_rule).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="删除规则", command=self.delete_rule).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="上移", command=lambda: self.move_rule(-1)).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="下移", command=lambda: self.move_rule(1)).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="保存", command=self.save_changes).pack(side=tk.LEFT)
        
        self.load_rules()
        
    def load_rules(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, rule in enumerate(self.ruleset_manager.rules):
            self.tree.insert('', 'end', values=(
                '✓' if rule.enabled else '✗',
                rule.pattern,
                rule.replacement,
                rule.comment
            ), tags=(str(idx),))
            
    def on_single_click(self, event):
        # 处理启用状态的点击
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            if column == "#1":  # 启用列
                index = int(self.tree.item(item, "tags")[0])
                self.ruleset_manager.rules[index].enabled = not self.ruleset_manager.rules[index].enabled
                self.load_rules()
                
    def on_double_click(self, event):
        # 处理其他列的编辑
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            column_index = int(column[1])-1
            if column_index == 0: return  # 启用列用单击处理
            
            # 创建编辑框
            x, y, width, height = self.tree.bbox(item, column)
            value = self.tree.item(item, "values")[column_index]
            
            self.entry = ttk.Entry(self.tree)
            self.entry.place(x=x, y=y, width=width, height=height)
            self.entry.insert(0, value)
            self.entry.focus()
            
            def save_edit(event):
                new_value = self.entry.get()
                index = int(self.tree.item(item, "tags")[0])
                # 更新对应字段
                if column_index == 1:
                    self.ruleset_manager.rules[index].pattern = new_value
                elif column_index == 2:
                    self.ruleset_manager.rules[index].replacement = new_value
                elif column_index == 3:
                    self.ruleset_manager.rules[index].comment = new_value
                self.load_rules()
                self.entry.destroy()
                
            self.entry.bind('<FocusOut>', save_edit)
            self.entry.bind('<Return>', save_edit)
            
    def filter_rules(self):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            text = ' '.join(map(str, values)).lower()
            self.tree.item(item, open=query in text)
            
    def add_rule(self):
        self.ruleset_manager.rules.append(Rule())
        self.load_rules()
        self.tree.yview_moveto(1)  # 自动滚动到底部
        
    def delete_rule(self):
        selected = self.tree.selection()
        if selected:
            index = int(self.tree.item(selected[0], 'tags')[0])
            del self.ruleset_manager.rules[index]
            self.load_rules()
            
    def move_rule(self, direction):
        selected = self.tree.selection()
        if selected:
            index = int(self.tree.item(selected[0], 'tags')[0])
            if 0 <= index + direction < len(self.ruleset_manager.rules):
                self.ruleset_manager.rules.insert(index + direction, self.ruleset_manager.rules.pop(index))
                self.load_rules()
                self.tree.selection_set(self.tree.get_children()[index + direction])
                
    def save_changes(self):
        if self.ruleset_manager.current_file:
            try:
                data = [rule.__dict__ for rule in self.ruleset_manager.rules]
                with open(self.ruleset_manager.current_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("保存成功", "规则已保存！")
                self.destroy()  # 保存后自动关闭窗口
            except Exception as e:
                messagebox.showerror("保存失败", str(e))
        else:
            messagebox.showwarning("未保存", "请先在规则集管理中选择保存位置")

class RuleSetManagerWindow(tk.Toplevel):
    def __init__(self, master, ruleset_manager):
        super().__init__(master)
        self.ruleset_manager = ruleset_manager
        self.title("规则集管理")
        self.geometry("800x500")
        
        # 文件列表
        self.tree = ttk.Treeview(self, columns=('name', 'path'), show='headings')
        self.tree.heading('name', text='规则集名称')
        self.tree.column('name', width=200)
        self.tree.heading('path', text='文件路径')
        self.tree.column('path', width=500)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="新建规则集", command=self.new_ruleset).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="打开规则集", command=self.open_ruleset).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="刷新列表", command=self.refresh_list).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="删除规则集", command=self.delete_ruleset).pack(side=tk.LEFT)
        
        self.refresh_list()
        
    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        try:
            for fname in os.listdir(self.ruleset_manager.ruleset_dir):
                if fname.endswith(".json"):
                    path = os.path.join(self.ruleset_manager.ruleset_dir, fname)
                    self.tree.insert("", "end", values=(fname[:-5], path))
        except Exception as e:
            messagebox.showerror("错误", f"无法读取规则集目录: {e}")
            
    def new_ruleset(self):
        new_win = tk.Toplevel(self)
        new_win.title("新建规则集")
        
        ttk.Label(new_win, text="规则集名称:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(new_win)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def confirm_create():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("错误", "名称不能为空")
                return
            
            path = os.path.join(self.ruleset_manager.ruleset_dir, f"{name}.json")
            if os.path.exists(path):
                messagebox.showwarning("错误", "同名规则集已存在")
                return
                
            try:
                with open(path, 'w') as f:
                    json.dump([], f)
                self.ruleset_manager.current_file = path
                self.ruleset_manager.rules = []
                self.master.update_title()
                self.refresh_list()
                new_win.destroy()
                messagebox.showinfo("成功", "规则集创建成功！")
            except Exception as e:
                messagebox.showerror("错误", f"创建失败: {e}")
                
        ttk.Button(new_win, text="创建", command=confirm_create).grid(row=1, columnspan=2)

    def open_ruleset(self):
        """打开选定规则集"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一个规则集")
            return
            
        path = self.tree.item(selected[0])['values'][1]
        try:
            # 使用安全加载方法
            data = self.ruleset_manager.safe_json_load(path)
            self.ruleset_manager.rules = [Rule(**item) for item in data]
            self.ruleset_manager.current_file = path
            self.master.update_title()
            messagebox.showinfo("成功", "规则集已加载！")
            self.destroy()
        except Exception as e:
            error_msg = f"加载失败: {str(e)}\n可能原因：\n1. 文件编码不匹配\n2. JSON格式错误\n3. 文件已损坏"
            messagebox.showerror("错误", error_msg)

    def save_ruleset(self):
        """保存规则集（统一使用UTF-8编码）"""
        if self.ruleset_manager.current_file:
            try:
                data = [rule.__dict__ for rule in self.ruleset_manager.rules]
                with open(self.ruleset_manager.current_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("保存成功", "规则已保存！")
            except Exception as e:
                messagebox.showerror("保存失败", str(e))
            
    def delete_ruleset(self):
        selected = self.tree.selection()
        if not selected:
            return
            
        path = self.tree.item(selected[0])['values'][1]
        if messagebox.askyesno("确认删除", "确定要删除这个规则集吗？"):
            try:
                os.remove(path)
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")

class TextConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("文本转换工具")
        self.geometry("1200x800")
        
        self.ruleset_manager = RuleSetManager()
        self.load_default_ruleset()  # 加载默认规则集
        
        # 菜单栏
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="管理规则集", command=self.open_ruleset_manager)
        file_menu.add_command(label="编辑当前规则集", command=self.open_rule_editor)
        
        # 主界面
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 文本编辑区
        self.input_text = tk.Text(main_frame, wrap=tk.WORD, font=('微软雅黑', 11))
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.auto_convert)
        
        # 转换结果区
        self.output_text = tk.Text(main_frame, wrap=tk.WORD, state=tk.DISABLED, font=('微软雅黑', 11))
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 复制按钮
        ttk.Button(self, text="复制结果到剪贴板", command=self.copy_result).pack(pady=10)
    
    def load_default_ruleset(self):
        try:
            with open(self.ruleset_manager.default_ruleset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.ruleset_manager.rules = [Rule(**item) for item in data]
                self.ruleset_manager.current_file = self.ruleset_manager.default_ruleset_path
                self.update_title()
        except Exception as e:
            messagebox.showerror("错误", f"加载默认规则集失败: {e}")
            
    def auto_convert(self, event=None):
        input_text = self.input_text.get("1.0", tk.END)
        converted = self.ruleset_manager.apply_rules(input_text)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", converted)
        self.output_text.config(state=tk.DISABLED)
        
    def copy_result(self):
        self.clipboard_clear()
        self.clipboard_append(self.output_text.get("1.0", tk.END))
        messagebox.showinfo("复制成功", "内容已复制到剪贴板！")
        
    def open_ruleset_manager(self):
        RuleSetManagerWindow(self, self.ruleset_manager)
        
    def open_rule_editor(self):
        if not self.ruleset_manager.current_file:
            messagebox.showwarning("提示", "请先创建或选择一个规则集")
            return
        RuleEditor(self, self.ruleset_manager)
        
    def update_title(self):
        if self.ruleset_manager.current_file:
            name = os.path.basename(self.ruleset_manager.current_file)[:-5]
            self.title(f"文本转换工具 - {name}")
        else:
            self.title("文本转换工具")

if __name__ == "__main__":
    app = TextConverterApp()
    app.mainloop()
