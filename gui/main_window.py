from __future__ import annotations
import json, threading, datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.core import (
    START_CONFIG_DEFAULT, TARGET_CONFIG, BoardState, parse_input_state, convert_state_to_string,
    check_solvability, generate_random_state
)
from algorithms.registry import ALGORITHM_GROUPS, HEURISTIC_ALGORITHMS

HISTORY_FILE = Path(__file__).resolve().parent.parent / 'history' / 'history.json'

class EightPuzzleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('8 Puzzle AI Solver')
        self.geometry('1120x820')
        self.minsize(1080, 760)
        self.configure(bg='#0f172a')
        self.path: list[BoardState] = []
        self.moves: list[str] = []
        self.current_step = 0
        self.playing = False
        self.after_id = None
        self.running = False
        self.history: list[dict] = []
        self.nav_buttons: list[ttk.Button] = []
        self._style()
        self._build_ui()
        self._load_history()
        self.draw_board(START_CONFIG_DEFAULT)
        self._refresh_algo_box()
        self._update_heuristic_state()
        self._set_nav_state('disabled')

    def _style(self):
        self.option_add('*TCombobox*Listbox.background', '#1e293b')
        self.option_add('*TCombobox*Listbox.foreground', '#f8fafc')
        self.option_add('*TCombobox*Listbox.selectBackground', '#0284c7')
        self.option_add('*TCombobox*Listbox.selectForeground', 'white')
        self.option_add('*TCombobox*Listbox.font', ('Segoe UI', 11))
        
        style = ttk.Style(self)
        try: style.theme_use('clam')
        except tk.TclError: pass
        style.configure('TFrame', background='#0f172a')
        style.configure('Card.TFrame', background='#1e293b', relief='flat')
        style.configure('TLabel', background='#0f172a', foreground='#f8fafc', font=('Segoe UI', 11))
        style.configure('Title.TLabel', background='#0f172a', foreground='#38bdf8', font=('Segoe UI', 22, 'bold'))
        style.configure('Sub.TLabel', background='#0f172a', foreground='#94a3b8', font=('Segoe UI', 11))
        style.configure('TLabelframe', background='#0f172a', relief='flat')
        style.configure('TLabelframe.Label', font=('Segoe UI', 12, 'bold'), foreground='#38bdf8', background='#0f172a')
        
        style.configure('TEntry', fieldbackground='#1e293b', foreground='white', bordercolor='#334155', lightcolor='#334155', darkcolor='#334155')
        style.configure('TCombobox', fieldbackground='#1e293b', foreground='white', background='#334155', arrowcolor='white', bordercolor='#334155')
        style.map('TCombobox', fieldbackground=[('readonly', '#1e293b')], foreground=[('readonly', 'white')])
        style.configure('TSpinbox', fieldbackground='#1e293b', foreground='white', background='#334155', arrowcolor='white', bordercolor='#334155')
        
        style.configure('TScale', background='#0f172a', troughcolor='#1e293b', sliderbackground='#0284c7', bordercolor='#0f172a', lightcolor='#0f172a', darkcolor='#0f172a')
        style.map('TScale', sliderbackground=[('active', '#38bdf8')])
        
        style.configure('TButton', font=('Segoe UI', 11), padding=6, background='#1e293b', foreground='white', bordercolor='#334155')
        style.map('TButton', 
                  background=[('active', '#334155'), ('disabled', '#0f172a')], 
                  foreground=[('active', 'white'), ('disabled', '#1e293b')], 
                  bordercolor=[('active', '#475569'), ('disabled', '#0f172a')],
                  lightcolor=[('active', '#475569'), ('disabled', '#0f172a')],
                  darkcolor=[('active', '#475569'), ('disabled', '#0f172a')])
                  
        style.configure('Accent.TButton', font=('Segoe UI', 11, 'bold'), padding=8, background='#0284c7', foreground='white', bordercolor='#0284c7')
        style.map('Accent.TButton', background=[('active', '#0369a1')], foreground=[('active', 'white')])
        
        style.configure('Treeview', rowheight=32, font=('Segoe UI', 10), background='#1e293b', fieldbackground='#1e293b', foreground='white')
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#334155', foreground='white', relief='flat')
        style.map('Treeview.Heading', background=[('active', '#475569')])

    def _build_ui(self):
        header = ttk.Frame(self, padding=(20, 10, 20, 5))
        header.pack(fill=tk.X)
        ttk.Label(header, text='8 Puzzle AI Solver', style='Title.TLabel').pack(anchor='w')
        ttk.Label(header, text='Hệ thống giải mã chuyên sâu tích hợp mô phỏng trực quan', style='Sub.TLabel').pack(anchor='w')

        main = ttk.Frame(self, padding=(20, 5, 20, 20))
        main.pack(fill=tk.BOTH, expand=True)
        
        left = ttk.Frame(main, width=400)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left.pack_propagate(False)
        
        right = ttk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        setup = ttk.LabelFrame(left, text='Thiết lập cấu hình', padding=10)
        setup.pack(fill=tk.X)
        self.start_var = tk.StringVar(value=convert_state_to_string(START_CONFIG_DEFAULT))
        self.goal_var = tk.StringVar(value=convert_state_to_string(TARGET_CONFIG))
        self.group_var = tk.StringVar(value='Informed Search')
        self.algorithm_var = tk.StringVar(value='A*')
        self.heuristic_var = tk.StringVar(value='Manhattan')
        self.depth_var = tk.IntVar(value=50)
        self.beam_var = tk.IntVar(value=15)
        self.max_nodes_var = tk.IntVar(value=300000)
        self.speed_ms = 500

        rows = [
            ('Trạng thái đầu', ttk.Entry(setup, textvariable=self.start_var, font=('Segoe UI', 11), width=25)),
            ('Trạng thái đích', ttk.Entry(setup, textvariable=self.goal_var, font=('Segoe UI', 11), width=25)),
            ('Nhóm thuật toán', ttk.Combobox(setup, textvariable=self.group_var, values=list(ALGORITHM_GROUPS), state='readonly', font=('Segoe UI', 11))),
            ('Thuật toán', ttk.Combobox(setup, textvariable=self.algorithm_var, state='readonly', font=('Segoe UI', 11))),
            ('Heuristic', ttk.Combobox(setup, textvariable=self.heuristic_var, values=['Manhattan', 'Số ô sai'], state='readonly', font=('Segoe UI', 11))),
            ('Depth limit / Vòng lặp', ttk.Spinbox(setup, from_=1, to=200, textvariable=self.depth_var, font=('Segoe UI', 11))),
            ('Beam / Restart', ttk.Spinbox(setup, from_=1, to=200, textvariable=self.beam_var, font=('Segoe UI', 11))),
            ('Giới hạn Node', ttk.Entry(setup, textvariable=self.max_nodes_var, font=('Segoe UI', 11))),
        ]
        for i, (label, widget) in enumerate(rows):
            ttk.Label(setup, text=label + ':', font=('Segoe UI', 11)).grid(row=i, column=0, sticky='w', pady=8, padx=(0, 10))
            widget.grid(row=i, column=1, sticky='ew', pady=8)
            
        ttk.Label(setup, text='Tốc độ mô phỏng:', font=('Segoe UI', 11)).grid(row=8, column=0, sticky='w', pady=8, padx=(0, 10))
        self.speed_canvas = tk.Canvas(setup, width=220, height=28, bg='#0f172a', highlightthickness=0)
        self.speed_canvas.grid(row=8, column=1, sticky='ew', pady=8)
        self.speed_ratio = 0.625
        self.speed_canvas.bind('<Button-1>', self._on_speed_click)
        self.speed_canvas.bind('<B1-Motion>', self._on_speed_click)
        self.speed_canvas.bind('<Configure>', lambda e: self._draw_speed_triangle())
        
        setup.columnconfigure(1, weight=1)
        rows[2][1].bind('<<ComboboxSelected>>', lambda e: self._refresh_algo_box())
        rows[3][1].bind('<<ComboboxSelected>>', lambda e: self._update_heuristic_state())

        actions = ttk.LabelFrame(left, text='Thao tác điều khiển', padding=10)
        actions.pack(fill=tk.X, pady=(15, 0))
        self.run_btn = ttk.Button(actions, text='▶  Chạy thuật toán AI', style='Accent.TButton', command=self.start_run)
        self.run_btn.pack(fill=tk.X, pady=4)
        ttk.Button(actions, text='🎲  Sinh trạng thái ngẫu nhiên', command=self.random_start).pack(fill=tk.X, pady=4)
        ttk.Button(actions, text='↺  Đặt lại mặc định', command=self.reset_default).pack(fill=tk.X, pady=4)
        ttk.Button(actions, text='📜  Xem lịch sử thực thi', style='Accent.TButton', command=self.open_history_window).pack(fill=tk.X, pady=(12, 4))

        board_box = ttk.LabelFrame(right, text='Mô phỏng bàn cờ trực quan', padding=5)
        board_box.pack(fill=tk.X, pady=(0, 10))
        self.board = tk.Canvas(board_box, width=470, height=470, bg='#0f172a', highlightthickness=0)
        self.board.pack(pady=2)

        controls = ttk.Frame(right)
        controls.pack(fill=tk.X, pady=5)
        
        btn_first = ttk.Button(controls, text='⏮ Đầu', command=self.first_step)
        btn_first.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        btn_prev = ttk.Button(controls, text='◀ Trước', command=self.prev_step)
        btn_prev.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        self.play_btn = ttk.Button(controls, text='▶ Play', command=self.toggle_play)
        self.play_btn.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        btn_next = ttk.Button(controls, text='Sau ▶', command=self.next_step)
        btn_next.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        btn_last = ttk.Button(controls, text='Cuối ⏭', command=self.last_step)
        btn_last.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        btn_replay = ttk.Button(controls, text='↺ Chạy lại', command=self.replay_simulation)
        btn_replay.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)
        
        self.nav_buttons = [btn_first, btn_prev, self.play_btn, btn_next, btn_last, btn_replay]

        self.status_var = tk.StringVar(value='Sẵn sàng.')
        ttk.Label(right, textvariable=self.status_var, wraplength=550, font=('Segoe UI', 12, 'bold'), foreground='#38bdf8').pack(anchor='w', pady=(5, 2))
        self.move_var = tk.StringVar(value='Bước: 0/0')
        ttk.Label(right, textvariable=self.move_var, font=('Segoe UI', 11), foreground='#94a3b8').pack(anchor='w', pady=(0, 5))

        result_box = ttk.LabelFrame(right, text='Thông số kết quả hiệu năng', padding=10)
        result_box.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.result_text = tk.Text(result_box, height=25, wrap='word', bg='#1e293b', fg='#f8fafc', insertbackground='white', relief='flat', font=('Consolas', 11))
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def _set_nav_state(self, state: str):
        for btn in self.nav_buttons:
            btn.configure(state=state)

    def _draw_speed_triangle(self):
        self.speed_canvas.delete('all')
        w = self.speed_canvas.winfo_width()
        h = self.speed_canvas.winfo_height()
        if w < 10: w = 220
        if h < 10: h = 28
        self.speed_canvas.create_polygon(0, h, w, h, w, 2, fill='#1e293b', outline='#334155', width=1)
        curr_x = int(self.speed_ratio * w)
        self.speed_canvas.create_polygon(0, h, curr_x, h, curr_x, h - int((h - 2) * self.speed_ratio), fill='#0284c7', outline='')
        self.speed_canvas.create_line(curr_x, 0, curr_x, h, fill='#38bdf8', width=2)
        self.speed_canvas.create_rectangle(curr_x - 3, h - 6, curr_x + 3, h, fill='white', outline='#0284c7')

    def _on_speed_click(self, event):
        w = self.speed_canvas.winfo_width()
        if w < 10: return
        x = max(0, min(event.x, w))
        self.speed_ratio = x / w
        min_ms = 80
        max_ms = 1200
        self.speed_ms = int(max_ms - self.speed_ratio * (max_ms - min_ms))
        self._draw_speed_triangle()

    def _refresh_algo_box(self):
        algos = list(ALGORITHM_GROUPS[self.group_var.get()].keys())
        cb = self._find_combo_for_var(self.algorithm_var)
        if cb: cb['values'] = algos
        if self.algorithm_var.get() not in algos: self.algorithm_var.set(algos[0])
        self._update_heuristic_state()

    def _find_combo_for_var(self, var):
        def walk(w):
            for ch in w.winfo_children():
                if isinstance(ch, ttk.Combobox) and str(ch.cget('textvariable')) == str(var): return ch
                r = walk(ch)
                if r: return r
        return walk(self)

    def _update_heuristic_state(self):
        cb = self._find_combo_for_var(self.heuristic_var)
        if cb: cb.configure(state='readonly' if self.algorithm_var.get() in HEURISTIC_ALGORITHMS else 'disabled')

    def draw_board(self, state: BoardState):
        self.board.delete('all')
        size = 140; gap = 12; ox = 13; oy = 13
        colors = {'tile': '#1e293b', 'blank': '#0f172a', 'text': '#38bdf8'}
        for i, v in enumerate(state):
            r, c = divmod(i, 3); x = ox + c * (size + gap); y = oy + r * (size + gap)
            fill = colors['blank'] if v == 0 else colors['tile']
            self.board.create_rectangle(x, y, x + size, y + size, fill=fill, outline='#334155', width=2)
            if v != 0:
                self.board.create_text(x + size / 2, y + size / 2, text=str(v), fill=colors['text'], font=('Segoe UI', 42, 'bold'))
        self.move_var.set(f'Bước: {self.current_step}/{max(0, len(self.path) - 1)}')

    def start_run(self):
        if self.running: return
        try:
            start = parse_input_state(self.start_var.get()); goal = parse_input_state(self.goal_var.get())
            if not check_solvability(start, goal):
                self._set_nav_state('disabled')
                messagebox.showerror('Không giải được', 'Trạng thái đầu và đích khác parity nghịch thế nên không giải được.'); return
        except Exception as e:
            messagebox.showerror('Lỗi nhập liệu', str(e)); return
        self.running = True; self.run_btn.configure(state='disabled'); self.status_var.set('Đang chạy thuật toán...')
        self._set_nav_state('disabled')
        threading.Thread(target=self._run_worker, args=(start, goal), daemon=True).start()

    def _run_worker(self, start, goal):
        group = self.group_var.get(); algo = self.algorithm_var.get(); fn = ALGORITHM_GROUPS[group][algo]
        try:
            r = fn(start, goal, heuristic=self.heuristic_var.get(), depth_limit=int(self.depth_var.get()),
                 beam_width=int(self.beam_var.get()), restarts=int(self.beam_var.get()), max_nodes=int(self.max_nodes_var.get()))
            if hasattr(r, 'algorithm_group'): r.algorithm_group = group
            else: setattr(r, 'group', group)
            if hasattr(r, 'algorithm_name'): r.algorithm_name = algo
            else: setattr(r, 'algorithm', algo)
            self.after(0, lambda: self._show_result(r, start, goal))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('Lỗi khi chạy', str(e)))
            self.after(0, self._finish_run)

    def _show_result(self, r, start, goal):
        is_found = getattr(r, 'is_found', getattr(r, 'found', False))
        state_history = getattr(r, 'state_history', getattr(r, 'path', [start]))
        action_list = getattr(r, 'action_list', getattr(r, 'moves', []))
        total_cost = getattr(r, 'total_cost', getattr(r, 'cost', 0))
        nodes_expanded = getattr(r, 'nodes_expanded', getattr(r, 'expanded', 0))
        nodes_generated = getattr(r, 'nodes_generated', getattr(r, 'generated', 0))
        peak_frontier_size = getattr(r, 'peak_frontier_size', getattr(r, 'max_frontier', 0))
        execution_time = getattr(r, 'execution_time', getattr(r, 'elapsed', 0.0))
        status_message = getattr(r, 'status_message', getattr(r, 'message', ''))
        algo_group = getattr(r, 'algorithm_group', getattr(r, 'group', ''))
        algo_name = getattr(r, 'algorithm_name', getattr(r, 'algorithm', ''))

        self.path = state_history or [start]
        self.moves = action_list
        self.current_step = 0
        self.draw_board(self.path[0])
        self.status_var.set(status_message)
        
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f'Nhóm: {algo_group}\nThuật toán: {algo_name}\n')
        self.result_text.insert(tk.END, f'Trạng thái đầu: {convert_state_to_string(start)}\nTrạng thái đích: {convert_state_to_string(goal)}\n')
        self.result_text.insert(tk.END, f'Tìm thấy: {"Có" if is_found else "Không"}\nCost/Số bước: {total_cost}\nExpanded: {nodes_expanded}\nGenerated: {nodes_generated}\nMax frontier: {peak_frontier_size}\nThời gian: {execution_time:.6f}s\n')
        self.result_text.insert(tk.END, 'Moves: ' + (', '.join(action_list) if action_list else '(trống)'))
        
        if is_found and len(self.path) > 1:
            self._set_nav_state('normal')
        else:
            self._set_nav_state('disabled')
            
        self._add_history_sync(is_found, state_history, action_list, total_cost, nodes_expanded, nodes_generated, peak_frontier_size, execution_time, status_message, algo_group, algo_name, start, goal)
        self._finish_run()

    def _finish_run(self):
        self.running = False; self.run_btn.configure(state='normal')

    def _add_history_sync(self, is_found, state_history, action_list, total_cost, nodes_expanded, nodes_generated, peak_frontier_size, execution_time, status_message, algo_group, algo_name, start, goal):
        item = {
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            'group': algo_group, 
            'algorithm': algo_name,
            'start': convert_state_to_string(start), 
            'goal': convert_state_to_string(goal), 
            'found': is_found, 
            'cost': total_cost,
            'expanded': nodes_expanded, 
            'generated': nodes_generated, 
            'elapsed': execution_time, 
            'message': status_message,
            'path': [convert_state_to_string(s) for s in state_history], 
            'moves': action_list
        }
        self.history.insert(0, item); self.history = self.history[:100]; self._save_history()
        if hasattr(self, 'history_tree') and self.history_tree.winfo_exists():
            self._render_history()

    def _load_history(self):
        if HISTORY_FILE.exists():
            try: self.history = json.loads(HISTORY_FILE.read_text(encoding='utf-8'))
            except Exception: self.history = []

    def _save_history(self):
        HISTORY_FILE.write_text(json.dumps(self.history, ensure_ascii=False, indent=2), encoding='utf-8')

    def open_history_window(self):
        win = tk.Toplevel(self)
        win.title('Lịch sử chạy thuật toán')
        win.geometry('1150x550')
        win.configure(bg='#0f172a')
        
        frame = ttk.LabelFrame(win, text='Danh sách lịch sử hệ thống', padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        cols = ('time', 'group', 'algorithm', 'start', 'goal', 'cost', 'expanded', 'generated', 'elapsed', 'status')
        self.history_tree = ttk.Treeview(frame, columns=cols, show='headings', height=12)
        
        headings = {
            'time': 'Thời gian', 'group': 'Nhóm thuật toán', 'algorithm': 'Thuật toán',
            'start': 'Start', 'goal': 'Goal', 'cost': 'Cost', 'expanded': 'Expanded',
            'generated': 'Generated', 'elapsed': 'Time(s)', 'status': 'Trạng thái'
        }
        widths = {'time': 140, 'group': 180, 'algorithm': 150, 'start': 90, 'goal': 90, 'cost': 60, 'expanded': 90, 'generated': 95, 'elapsed': 90, 'status': 90}
        
        for c in cols:
            self.history_tree.heading(c, text=headings[c])
            self.history_tree.column(c, width=widths[c], minwidth=widths[c], anchor='w', stretch=False)
            
        ybar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        xbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky='nsew')
        ybar.grid(row=0, column=1, sticky='ns')
        xbar.grid(row=1, column=0, sticky='ew')
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        ttk.Button(btn_frame, text='🗑  Xóa toàn bộ lịch sử', command=self.clear_history).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text='📥  Tải lại bảng ghi chọn', command=self.load_history_item).pack(side=tk.RIGHT, padx=5)
        
        self._render_history()

    def _render_history(self):
        if hasattr(self, 'history_tree') and self.history_tree.winfo_exists():
            self.history_tree.delete(*self.history_tree.get_children())
            for idx, item in enumerate(self.history):
                self.history_tree.insert('', tk.END, iid=str(idx), values=(
                    item.get('time', ''), item.get('group', 'N/A'), item.get('algorithm', 'N/A'), item.get('start', ''), item.get('goal', ''),
                    item.get('cost', ''), item.get('expanded', ''), item.get('generated', ''),
                    f"{item.get('elapsed', 0):.6f}" if isinstance(item.get('elapsed', 0), (int, float)) else item.get('elapsed', ''),
                    'OK' if item.get('found') else 'Fail'
                ))

    def load_history_item(self, event=None):
        if not hasattr(self, 'history_tree') or not self.history_tree.winfo_exists(): return
        sel = self.history_tree.selection()
        if not sel:
            messagebox.showwarning('Thông báo', 'Vui lòng chọn một dòng lịch sử trong bảng trước.'); return
        item = self.history[int(sel[0])]
        self.start_var.set(item.get('start', '')); self.goal_var.set(item.get('goal', '')); self.group_var.set(item.get('group', 'Informed Search')); self._refresh_algo_box(); self.algorithm_var.set(item.get('algorithm', 'A*'))
        self.path = [parse_input_state(s) for s in item.get('path', [])] or [parse_input_state(item.get('start', convert_state_to_string(START_CONFIG_DEFAULT)))]
        self.moves = item.get('moves', []); self.current_step = 0; self.draw_board(self.path[0])
        self.status_var.set('Đã tải lại lịch sử: ' + item.get('message', ''))
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, json.dumps(item, ensure_ascii=False, indent=2))
        if item.get('found') and len(self.path) > 1:
            self._set_nav_state('normal')
        else:
            self._set_nav_state('disabled')

    def clear_history(self):
        if messagebox.askyesno('Xác nhận', 'Bạn có chắc chắn muốn xóa toàn bộ lịch sử dữ liệu không?'):
            self.history = []; self._save_history()
            if hasattr(self, 'history_tree') and self.history_tree.winfo_exists():
                self.history_tree.delete(*self.history_tree.get_children())
            self.status_var.set('Đã xóa lịch sử.')

    def random_start(self):
        self.start_var.set(convert_state_to_string(generate_random_state(TARGET_CONFIG, 70)))
        self.draw_board(parse_input_state(self.start_var.get()))
        self._set_nav_state('disabled')

    def reset_default(self):
        self.start_var.set(convert_state_to_string(START_CONFIG_DEFAULT))
        self.goal_var.set(convert_state_to_string(TARGET_CONFIG))
        self.group_var.set('Informed Search')
        self._refresh_algo_box()
        self.algorithm_var.set('A*')
        self.path = []; self.moves = []; self.current_step = 0
        self.draw_board(START_CONFIG_DEFAULT)
        self.status_var.set('Đã reset mặc định.')
        self._set_nav_state('disabled')

    def first_step(self):
        if self.path: self.current_step = 0; self.draw_board(self.path[0])
    def last_step(self):
        if self.path: self.current_step = len(self.path) - 1; self.draw_board(self.path[-1])
    def prev_step(self):
        if self.path and self.current_step > 0: self.current_step -= 1; self.draw_board(self.path[self.current_step])
    def next_step(self):
        if self.path and self.current_step < len(self.path) - 1: self.current_step += 1; self.draw_board(self.path[self.current_step])
    def toggle_play(self):
        if not self.path: return
        self.playing = not self.playing; self.play_btn.configure(text='⏸ Pause' if self.playing else '▶ Play')
        if self.playing: self._play_loop()
    def _play_loop(self):
        if not self.playing: return
        if self.current_step >= len(self.path) - 1:
            self.playing = False; self.play_btn.configure(text='▶ Play'); return
        self.next_step(); self.after_id = self.after(self.speed_ms, self._play_loop)
    def replay_simulation(self):
        if not self.path: return
        if self.after_id: self.after_cancel(self.after_id)
        self.current_step = 0
        self.draw_board(self.path[0])
        self.playing = True
        self.play_btn.configure(text='⏸ Pause')
        self._play_loop()