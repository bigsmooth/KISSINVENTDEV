# =========================
# SECTION 1 — Setup & Language
# =========================
import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import io
import shutil
from datetime import datetime
from pathlib import Path
import shutil


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# --- Language selector (EN / 中文) ---
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

lang = st.sidebar.selectbox("🌐 Language", ["English", "中文"],
                            index=0 if st.session_state["lang"] == "en" else 1)
st.session_state["lang"] = "en" if lang == "English" else "zh"

translations = {
    "en": {
        "supplier_shipments": "🚚 Supplier Shipments",
        "add_skus": "Add one or more SKUs for this shipment.",
        "tracking_number": "Tracking Number",
        "carrier": "Carrier Name",
        "destination_hub": "Destination Hub",
        "shipping_date": "Shipping Date",
        "sku": "SKU",
        "qty": "Qty",
        "remove": "Remove",
        "add_another_sku": "Add Another SKU",
        "create_new_sku": "➕ Create New SKU",
        "new_sku_name": "New SKU Name",
        "add_sku": "Add SKU",
        "submit_shipment": "Submit Shipment",
        "shipment_submitted": "Shipment submitted successfully!",
        "fill_out_required": "Please fill out all required fields and SKUs.",
        "your_shipments": "📦 Your Shipments",
        "no_shipments": "You have not submitted any shipments yet.",
        "incoming_shipments": "📦 Incoming Shipments to Your Hub",
        "mark_received": "Mark Shipment as Received",
        "confirm_receipt": "Confirm receipt of shipment",
        "delete_shipment": "Delete Shipment",
        "confirm_delete": "Confirm delete shipment",
        "shipment_deleted": "Shipment deleted.",
        "shipment_confirmed": "Shipment confirmed received and inventory updated.",
        "restock_orders": "🔄 Restock Orders",
        "create_user": "➕ Create User",
        "user_created": "User created successfully!",
        "select_user": "Select User",
        "remove_user": "Remove User",
        "confirm_remove_user": "Really remove",
        "user_removed": "User removed.",
        "backup": "🗄️ Backup Database",
        "restore": "🔄 Restore Database",
        "download_backup": "Download Backup CSV",
        "upload_csv": "Upload CSV for Restore",
        "count_confirmed": "Count confirmed.",
        "refresh": "Refresh",
        "update_inventory": "Update Inventory",
        "select_sku": "Select SKU",
        "action": "Action",
        "quantity": "Quantity",
        "optional_comment": "Optional Comment",
        "submit_update": "Submit Update",
        "bulk_update": "Bulk Inventory Update",
        "adjust_quantity": "Adjust Quantity (+IN / -OUT)",
        "comment": "Comment",
        "apply_updates": "Apply All Updates",
        "sku_exists": "SKU already exists!",
        "enter_sku_name": "Please enter a SKU name.",
        "create_sku": "Create SKU",
        "upload_skus": "Upload SKUs from CSV",
        "assign_skus": "Assign SKUs to Hubs",
        "select_sku_assign": "Select SKU to Assign",
        "assign_to_hubs": "Assign to Hubs",
        "update_assignments": "Update Assignments",
        "assignment_updated": "SKU assignment updated!",
        "manage_users": "Manage Users",
        "username": "Username",
        "role": "Role",
        "hub": "Hub",
        "send_message": "Send Message",
        "to": "To",
        "subject": "Subject",
        "message": "Message",
        "send": "Send",
        "your_threads": "Your Threads",
        "reply": "Reply",
        "send_reply": "Send Reply",
        "only_reply_hq": "Only reply to HQ is allowed.",
        "activity_logs": "Activity Logs",
        "filter_logs": "Filter logs",
        "inventory_count_mode": "Inventory Count Mode",
        "confirmed_counts": "Confirmed Counts",
        "export_inventory": "Export Inventory",
    },
    "zh": {
        "supplier_shipments": "🚚 供应商发货",
        "add_skus": "为此发货添加一个或多个SKU。",
        "tracking_number": "追踪号码",
        "carrier": "承运人名称",
        "destination_hub": "目的中心",
        "shipping_date": "发货日期",
        "sku": "SKU",
        "qty": "数量",
        "remove": "移除",
        "add_another_sku": "添加另一个SKU",
        "create_new_sku": "➕ 新建SKU",
        "new_sku_name": "新SKU名称",
        "add_sku": "添加SKU",
        "submit_shipment": "提交发货",
        "shipment_submitted": "发货已成功提交！",
        "fill_out_required": "请填写所有必填字段和SKU。",
        "your_shipments": "📦 您的发货记录",
        "no_shipments": "您还没有提交任何发货。",
        "incoming_shipments": "📦 您中心的待发货记录",
        "mark_received": "标记发货为已收到",
        "confirm_receipt": "确认收货",
        "delete_shipment": "删除发货",
        "confirm_delete": "确认删除发货",
        "shipment_deleted": "发货已删除。",
        "shipment_confirmed": "发货已确认收到，库存已更新。",
        "restock_orders": "🔄 补货订单",
        "create_user": "➕ 创建用户",
        "user_created": "用户创建成功！",
        "select_user": "选择用户",
        "remove_user": "删除用户",
        "confirm_remove_user": "确认删除",
        "user_removed": "用户已删除。",
        "backup": "🗄️ 数据库备份",
        "restore": "🔄 数据库恢复",
        "download_backup": "下载备份CSV",
        "upload_csv": "上传CSV以恢复",
        "count_confirmed": "库存盘点已确认。",
        "refresh": "刷新",
        "update_inventory": "更新库存",
        "select_sku": "选择SKU",
        "action": "操作",
        "quantity": "数量",
        "optional_comment": "可选备注",
        "submit_update": "提交更新",
        "bulk_update": "批量库存更新",
        "adjust_quantity": "调整数量（+入库 / -出库）",
        "comment": "备注",
        "apply_updates": "应用所有更新",
        "sku_exists": "SKU已存在！",
        "enter_sku_name": "请输入SKU名称。",
        "create_sku": "创建SKU",
        "upload_skus": "从CSV上传SKU",
        "assign_skus": "分配SKU到仓库",
        "select_sku_assign": "选择要分配的SKU",
        "assign_to_hubs": "分配到仓库",
        "update_assignments": "更新分配",
        "assignment_updated": "SKU分配已更新！",
        "manage_users": "管理用户",
        "username": "用户名",
        "role": "角色",
        "hub": "仓库",
        "send_message": "发送消息",
        "to": "收件人",
        "subject": "主题",
        "message": "消息",
        "send": "发送",
        "your_threads": "您的会话",
        "reply": "回复",
        "send_reply": "发送回复",
        "only_reply_hq": "只能回复总部。",
        "activity_logs": "活动日志",
        "filter_logs": "筛选日志",
        "inventory_count_mode": "库存盘点模式",
        "confirmed_counts": "已确认盘点",
        "export_inventory": "导出库存",
    }
}

def T(key: str) -> str:
    return translations[st.session_state["lang"]].get(key, key)

# --- Paths ---
APP_DIR = Path(__file__).parent
DB = APP_DIR / "ttt_inventory.db"
SNAP_DIR = APP_DIR / "snapshots"
SNAP_DIR.mkdir(exist_ok=True)

# --- Hash helper ---
def hash_pw(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

# --- DB helpers ---
def _connect():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def query(sql: str, params=(), fetch: bool = True, commit: bool = True):
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        if commit:
            conn.commit()
        return cur.fetchall() if fetch else None

# --- One-click DB snapshot/restore ---
def snapshot_db(label: str = "") -> Path | None:
    """Copy DB to snapshots/ with timestamp (no overwrite)."""
    if not DB.exists():
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"-{label}" if label else ""
    out = SNAP_DIR / f"ttt_inventory_{ts}{suffix}.db"
    shutil.copy2(DB, out)
    return out

def restore_db(snapshot_path: Path) -> None:
    """Restore DB from a snapshot file."""
    if snapshot_path and snapshot_path.exists():
        shutil.copy2(snapshot_path, DB)



# =========================
# SECTION 2 — Database Setup & Seeding
# =========================

# --- Create tables (safe, no wipe) ---
# --- DB Setup & Seeding ---
def create_tables():
    query("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT,
        hub TEXT)""")

    query("""CREATE TABLE IF NOT EXISTS inventory (
        sku TEXT,
        hub TEXT,
        quantity INTEGER,
        PRIMARY KEY (sku, hub))""")

    query("""CREATE TABLE IF NOT EXISTS logs (
        timestamp TEXT,
        user TEXT,
        sku TEXT,
        hub TEXT,
        action TEXT,
        qty INTEGER,
        comment TEXT)""")

    query("""CREATE TABLE IF NOT EXISTS sku_info (
        sku TEXT PRIMARY KEY,
        product_name TEXT,
        assigned_hubs TEXT)""")

    query("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        recipient TEXT,
        subject TEXT,
        message TEXT,
        timestamp TEXT,
        thread_id TEXT,
        reply_to INTEGER)""")

    query("""CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier TEXT,
        tracking TEXT,
        carrier TEXT,
        hub TEXT,
        date TEXT,
        status TEXT DEFAULT 'Pending')""")

    query("""CREATE TABLE IF NOT EXISTS shipment_items (
        shipment_id INTEGER,
        sku TEXT,
        qty INTEGER)""")

    query("""CREATE TABLE IF NOT EXISTS count_confirmations (
        sku TEXT,
        hub TEXT,
        count INTEGER,
        confirmed_by TEXT,
        timestamp TEXT)""")


def seed_users():
    users = [
        ("kevin", hash_pw("admin123"), "Admin", "HQ"),
        ("slo",   hash_pw("hub1pass"), "Hub Manager", "Hub 1"),
        ("fox",   hash_pw("hub2pass"), "Hub Manager", "Hub 2"),
        ("carmen",hash_pw("hub3pass"), "Hub Manager", "Hub 3"),
        ("smooth",hash_pw("retailpass"), "Retail", "Retail")
    ]
    for u in users:
        query("INSERT OR IGNORE INTO users (username, password, role, hub) VALUES (?, ?, ?, ?)", u, fetch=False)


def seed_all_skus():
    # keep your existing SKU seeding function body here (unchanged)
    pass  # <- replace with your real seeding code


def setup_db():
    create_tables()
    # only seed when empty
    if not query("SELECT 1 FROM users LIMIT 1"):
        seed_users()
    if not query("SELECT 1 FROM sku_info LIMIT 1"):
        seed_all_skus()


# --- SKU Seeder ---
def seed_all_skus():
    # Only seed if sku_info table empty
    if query("SELECT COUNT(*) FROM sku_info")[0][0] > 0:
        return

    hub_assignments = {
        "Hub 1": [
            "All American Stripes", "Carolina Blue and White Stripes", "Navy and Silver Stripes",
            "Black and Hot Pink Stripes", "Bubble Gum and White Stripes", "White and Ice Blue Stripes",
            "Imperial Purple and White Stripes", "Hot Pink and White Stripes", "Rainbow Stripes",
            "Twilight Pop", "Juicy Purple", "Lovely Lilac", "Black", "Black and White Stripes"
        ],
        "Hub 2": [
            "Black and Yellow Stripes", "Orange and Black Stripes", "Black and Purple Stripes",
            "Electric Blue and White Stripes", "Blossom Breeze", "Candy Cane Stripes",
            "Plum Solid", "Patriots (Custom)", "Snow Angel (Custom)", "Cranberry Frost (Custom)",
            "Witchy Vibes", "White and Green Stripes", "Black Solid", "Black and White Stripes", "Black and Orange Stripes"
        ],
        "Hub 3": [
            "Black and Grey Stripes", "Black and Green Stripes", "Smoke Grey and Black Stripes",
            "Black and Red Stripes", "Black and Purple Stripes", "Dark Cherry and White Stripes", "Black and Multicolor Stripes",
            "Puerto Rican (Custom)", "Seahawks (Custom)", "PCH (Custom)", "Valentine Socks",
            "Rainbow Stripes", "Thin Black Socks", "Thin Black and White Stripes", "Smoke Grey Solid",
            "Cherry Solid", "Brown Solid", "Wheat and White Stripes", "Black Solid", "Black and White Stripes"
        ],
        "Retail": [  # Retail gets all SKUs from all hubs
            "All American Stripes", "Carolina Blue and White Stripes", "Navy and Silver Stripes",
            "Black and Hot Pink Stripes", "Bubble Gum and White Stripes", "White and Ice Blue Stripes",
            "Imperial Purple and White Stripes", "Hot Pink and White Stripes", "Rainbow Stripes",
            "Twilight Pop", "Juicy Purple", "Lovely Lilac", "Black", "Black and White Stripes",
            "Black and Yellow Stripes", "Orange and Black Stripes", "Black and Purple Stripes",
            "Electric Blue and White Stripes", "Blossom Breeze", "Candy Cane Stripes",
            "Plum Solid", "Patriots (Custom)", "Snow Angel (Custom)", "Cranberry Frost (Custom)",
            "Witchy Vibes", "White and Green Stripes", "Black Solid", "Black and White Stripes",
            "Black and Grey Stripes", "Black and Green Stripes", "Smoke Grey and Black Stripes",
            "Black and Red Stripes", "Dark Cherry and White Stripes", "Black and Multicolor Stripes",
            "Puerto Rican (Custom)", "Seahawks (Custom)", "PCH (Custom)", "Valentine Socks",
            "Thin Black Socks", "Thin Black and White Stripes", "Smoke Grey Solid", "Cherry Solid",
            "Brown Solid", "Wheat and White Stripes"
        ]
    }

    for hub, skus in hub_assignments.items():
        for sku in skus:
            query(
                "INSERT OR IGNORE INTO sku_info (sku, product_name, assigned_hubs) VALUES (?, ?, ?)",
                (sku, sku, hub),
                fetch=False
            )
            # Also ensure inventory rows exist
            query(
                "INSERT OR IGNORE INTO inventory (sku, hub, quantity) VALUES (?, ?, ?)",
                (sku, hub, 0),
                fetch=False
            )


# --- Ensure DB ready before UI ---
def ensure_db_ready():
    # Take startup snapshot once per session
    if "took_startup_snapshot" not in st.session_state and DB.exists():
        snap = snapshot_db("startup")
        if snap:
            st.session_state["took_startup_snapshot"] = str(snap)

    create_tables()
    seed_users()
    seed_all_skus()


# Run DB setup immediately
ensure_db_ready()

# =========================
# SECTION 2.5 — Initialize DB (call AFTER setup_db is defined)
# =========================
if "db_init" not in st.session_state:
    setup_db()              # creates tables; seeds only if empty
    st.session_state["db_init"] = True


# =========================
# SECTION 3 — Login & Role Setup
# =========================

# --- Small helpers used by multiple sections ---
def get_all_hubs():
    rows = query("SELECT DISTINCT hub FROM inventory")
    hubs = sorted({r[0] for r in rows if r[0]})
    for extra in ["Hub 1", "Hub 2", "Hub 3", "Retail", "HQ"]:
        if extra not in hubs:
            hubs.append(extra)
    return hubs

def is_sku_assigned_to_hub(sku: str, hub: str) -> bool:
    row = query("SELECT assigned_hubs FROM sku_info WHERE sku=?", (sku,))
    if not row or not row[0][0]:
        return False
    assigned = [h.strip() for h in row[0][0].split(",") if h.strip()]
    return hub in assigned

# --- Login panel ---
def login_panel():
    st.title("🔐 Login")
    col1, col2 = st.columns([1,1])
    with col1:
        u = st.text_input("Username", key="login_user")
    with col2:
        p = st.text_input("Password", type="password", key="login_pw")

    if st.button("Login", key="login_btn"):
        hashed = hash_pw(p)
        res = query("SELECT username, role, hub FROM users WHERE username=? AND password=?", (u, hashed))
        if res:
            st.session_state["user"] = res[0][0]
            st.session_state["role"] = res[0][1]
            st.session_state["hub"]  = res[0][2]
            st.success("✅ Logged in")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# If not logged in, stop here
if "user" not in st.session_state:
    login_panel()
    st.stop()

# --- Logged-in identity ---
username = st.session_state["user"]
role     = st.session_state["role"]
hub      = st.session_state["hub"]

# --- Sidebar identity & logout ---
st.sidebar.markdown(f"👤 **{username}**  \n🛠️ {role}")
if hub:
    st.sidebar.markdown(f"🏠 {hub}")

if st.sidebar.button("🚪 Logout", key=f"logout_btn_{username}"):
    for k in ["user", "role", "hub"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

# =========================
# SECTION 4 — Menus & Inventory
# =========================

# --- Menus by role ---
ADMIN_TABS = [
    "Inventory", "Update Stock", "Logs", "History", "Messages",
    "Shipments", "Create SKU", "Upload CSV", "Assign SKUs",
    "Manage Users", "Inventory Count", "Backup"
]
HUB_TABS = ["Inventory", "Update Stock", "Logs", "History", "Messages", "Shipments", "Inventory Count"]
RETAIL_TABS = HUB_TABS
SUPPLIER_TABS = [T("supplier_shipments")]

TABS_BY_ROLE = {
    "Admin": ADMIN_TABS,
    "Hub Manager": HUB_TABS,
    "Retail": RETAIL_TABS,
    "Supplier": SUPPLIER_TABS
}

menu = st.sidebar.radio("📂 Menu", TABS_BY_ROLE.get(role, []), key="menu_radio")

# --- Inventory page ---
if menu == "Inventory":
    st.header("📦 Inventory")

    # Which hub to view?
    if role == "Admin":
        hub_to_view = st.selectbox("Select Hub", sorted(get_all_hubs()), key="inv_hub_select")
    else:
        hub_to_view = hub
        st.info(f"Viewing inventory for **{hub_to_view}**")

    # Optional search
    search = st.text_input("🔎 Search SKU or Product name (optional)", key="inv_search").strip().lower()

    # Load base data
    sku_name_pairs = query("SELECT sku, product_name FROM sku_info")
    name_map = {s: (n or "") for s, n in sku_name_pairs}

    inv_rows = query("SELECT sku, quantity FROM inventory WHERE hub = ?", (hub_to_view,))
    records = []
    for s, q in inv_rows:
        pname = name_map.get(s, "")
        if search and (search not in s.lower() and search not in pname.lower()):
            continue
        status = "🟥 Low" if (q or 0) < 10 else "✅ OK"
        records.append((s, pname, q, status))

    df = pd.DataFrame(records, columns=["SKU", "Product Name", "Qty", "Status"]).sort_values("SKU")
    if df.empty:
        st.warning("No inventory records match your filters.")
    else:
        st.dataframe(df, use_container_width=True, key="inventory_df")

        # Export
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            "📥 Export Inventory CSV",
            csv_buf.getvalue(),
            file_name=f"inventory_{hub_to_view}.csv",
            mime="text/csv",
            key="inventory_export_btn"
        )

# --- Sidebar Menu ---
tabs_by_role = {
    "Admin": [
        "Inventory", "Update Stock", "Logs", "History", "Messages",
        "Shipments", "Create SKU", "Upload CSV", "Assign SKUs",
        "Manage Users", "Inventory Count", "Backup"
    ],
    "Hub Manager": [
        "Inventory", "Update Stock", "Logs", "History", "Messages",
        "Shipments", "Inventory Count"
    ],
    "Retail": [
        "Inventory", "Update Stock", "Logs", "History", "Messages",
        "Shipments", "Inventory Count"
    ],
    "Supplier": [T("supplier_shipments")]
}

menu = st.sidebar.radio("📂 Menu", tabs_by_role.get(role, []), key="main_menu")

# --- Inventory Tab ---
if menu == "Inventory":
    st.header("📦 Inventory")

    # Hub selection for Admin only
    hub_to_view = hub if role != "Admin" else st.selectbox(
        "Select Hub", sorted(get_all_hubs()), key="inv_hub"
    )

    search = st.text_input("Search SKU or Product", key="inv_search")

    all_skus = query("SELECT sku, product_name FROM sku_info")
    sku_filter = [
        sku for sku, name in all_skus
        if search.lower() in sku.lower() or search.lower() in name.lower()
    ] if search else None

    inventory_data = query(
        "SELECT sku, quantity FROM inventory WHERE hub = ?", (hub_to_view,)
    )
    sku_map = dict(all_skus)

    filtered = [
        (sku, qty, sku_map.get(sku, ""))
        for sku, qty in inventory_data
        if not sku_filter or sku in sku_filter
    ]

    df = pd.DataFrame(filtered, columns=["SKU", "Quantity", "Product Name"])\
             .sort_values(by="SKU")
    st.dataframe(df, use_container_width=True)

# --- Update Stock Tab ---
if menu == "Update Stock":
    st.header("🔁 Update Inventory")

    # Get SKUs and map to names
    sku_list = query("SELECT sku, product_name FROM sku_info")
    sku_map = {sku: name for sku, name in sku_list}

    # Hub selection for Admin only
    hub_view = hub if role != "Admin" else st.selectbox(
        "Select Hub", sorted(get_all_hubs()), key="upd_hub"
    )

    # Show only SKUs assigned to hub
    assigned_skus = [
        f"{s} - {sku_map[s]}"
        for s in sku_map if is_sku_assigned_to_hub(s, hub_view)
    ]

    sku = st.selectbox("Select SKU", assigned_skus, key="upd_sku")
    action = st.radio("Action", ["IN", "OUT"], horizontal=True, key="upd_action")
    qty = st.number_input("Quantity", min_value=1, step=1, key="upd_qty")
    comment = st.text_input("Optional Comment", key="upd_comment")

    if st.button("Submit Update", key="upd_submit"):
        sku_code = sku.split(" - ")[0]
        current_qty = query(
            "SELECT quantity FROM inventory WHERE sku = ? AND hub = ?",
            (sku_code, hub_view)
        )
        current = current_qty[0][0] if current_qty else 0
        new_qty = current + qty if action == "IN" else current - qty

        if new_qty < 0:
            st.warning("❌ Not enough stock to remove.")
        else:
            # Update inventory
            query(
                "UPDATE inventory SET quantity = ? WHERE sku = ? AND hub = ?",
                (new_qty, sku_code, hub_view), fetch=False
            )
            # Log action
            query(
                "INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?)",
                (datetime.now(), username, sku_code, hub_view, action, qty, comment),
                fetch=False
            )
            st.success(f"✅ {action} action submitted for {sku_code} ({qty})")


# --- Logs Tab ---
if menu == "Logs":
    st.header("📜 Activity Logs")

    # Pull logs
    rows = query("SELECT * FROM logs ORDER BY timestamp DESC")
    df = pd.DataFrame(
        rows,
        columns=["Time", "User", "SKU", "Hub", "Action", "Qty", "Comment"]
    )

    if df.empty:
        st.info("No activity yet.")
    else:
        # Format time
        try:
            df["Time"] = pd.to_datetime(df["Time"]).dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            pass

        # Quick filters
        with st.expander("🔍 Filter logs"):
            col1, col2, col3, col4 = st.columns(4)
            user_filter = col1.selectbox(
                "User", ["All"] + sorted(df["User"].unique().tolist()), index=0
            )
            action_filter = col2.selectbox("Action", ["All", "IN", "OUT"], index=0)
            sku_filter = col3.selectbox(
                "SKU", ["All"] + sorted(df["SKU"].unique().tolist()), index=0
            )
            text_filter = col4.text_input("Text search", placeholder="SKU, comment…")

        # Apply filters
        filtered = df.copy()
        if role != "Admin":
            filtered = filtered[filtered["Hub"] == hub]
        if user_filter != "All":
            filtered = filtered[filtered["User"] == user_filter]
        if action_filter != "All":
            filtered = filtered[filtered["Action"] == action_filter]
        if sku_filter != "All":
            filtered = filtered[filtered["SKU"] == sku_filter]
        if text_filter:
            tl = text_filter.lower()
            filtered = filtered[
                filtered.apply(lambda r: tl in " ".join(map(str, r.values)).lower(), axis=1)
            ]

        st.dataframe(filtered, use_container_width=True)

        # Download CSV of what's shown
        csv_bytes = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download filtered CSV",
            csv_bytes,
            "logs_filtered.csv",
            "text/csv",
            key="download_logs_csv",
        )

# --- Inventory Count Tab ---
if menu == "Inventory Count":
    st.header("🧾 Inventory Count")

    if role != "Admin":
        # SKUs assigned to this hub
        sku_rows = query(
            "SELECT sku FROM sku_info WHERE INSTR(assigned_hubs, ?) > 0 ORDER BY sku",
            (hub,)
        )
        sku_options = [r[0] for r in sku_rows]

        if not sku_options:
            st.info("No SKUs assigned to your hub yet.")
        else:
            with st.form("count_form"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    count_sku = st.selectbox("Select SKU", sku_options, key="count_sku_select")
                with c2:
                    counted_qty = st.number_input("Counted Qty", min_value=0, step=1, key="count_qty_input")
                note = st.text_input("Comment (optional)", key="count_comment")
                submitted = st.form_submit_button("✅ Confirm Count")
                if submitted:
                    query(
                        "INSERT INTO count_confirmations (sku, hub, count, confirmed_by, timestamp) VALUES (?, ?, ?, ?, ?)",
                        (count_sku, hub, int(counted_qty), username, datetime.now().isoformat()),
                        fetch=False
                    )
                    st.success(f"Count for **{count_sku}** recorded as **{counted_qty}**.")

        st.subheader("Recent confirmations (yours)")
        mine = query(
            "SELECT sku, count, timestamp, confirmed_by FROM count_confirmations WHERE hub=? AND confirmed_by=? ORDER BY timestamp DESC LIMIT 20",
            (hub, username)
        )
        if mine:
            df_mine = pd.DataFrame(mine, columns=["SKU", "Count", "Time", "User"])
            st.dataframe(df_mine, use_container_width=True)
            st.download_button(
                "📥 Download your counts (CSV)",
                df_mine.to_csv(index=False).encode("utf-8"),
                file_name=f"counts_{hub}_{username}.csv",
                mime="text/csv",
                key="dl_mycnts_csv"
            )
        else:
            st.info("No confirmations yet.")

    else:
        # Admin view
        st.subheader("All confirmed counts")
        rows = query("SELECT sku, hub, count, confirmed_by, timestamp FROM count_confirmations ORDER BY timestamp DESC")
        if not rows:
            st.info("No confirmations recorded yet.")
        else:
            df = pd.DataFrame(rows, columns=["SKU", "Hub", "Count", "User", "Time"])

            with st.expander("🔍 Filters"):
                col1, col2, col3 = st.columns(3)
                hub_f = col1.selectbox("Hub", ["All"] + sorted(df["Hub"].unique().tolist()), index=0, key="cnt_hub_f")
                user_f = col2.selectbox("User", ["All"] + sorted(df["User"].unique().tolist()), index=0, key="cnt_user_f")
                sku_f = col3.selectbox("SKU", ["All"] + sorted(df["SKU"].unique().tolist()), index=0, key="cnt_sku_f")

            filtered = df.copy()
            if hub_f != "All":
                filtered = filtered[filtered["Hub"] == hub_f]
            if user_f != "All":
                filtered = filtered[filtered["User"] == user_f]
            if sku_f != "All":
                filtered = filtered[filtered["SKU"] == sku_f]

            st.dataframe(filtered, use_container_width=True)

            st.download_button(
                "📥 Download counts (CSV)",
                filtered.to_csv(index=False).encode("utf-8"),
                file_name="counts_confirmations.csv",
                mime="text/csv",
                key="dl_counts_csv"
            )

# --- Messages Tab ---
if menu == "Messages":
    st.header("💬 Messages")

    # Load threads where the user is sender or recipient
    threads = query("""
        SELECT thread_id, subject, MAX(timestamp) as last_time
        FROM messages
        WHERE sender=? OR recipient=?
        GROUP BY thread_id, subject
        ORDER BY last_time DESC
    """, (username, username))

    # Start a new message
    with st.expander("✉️ Send New Message"):
        # Admin can message anyone, others only to Admin
        if role == "Admin":
            recipients = [u[0] for u in query("SELECT username FROM users WHERE username != ?", (username,))]
        else:
            recipients = [u[0] for u in query("SELECT username FROM users WHERE role='Admin'")]
        to_user = st.selectbox("To", recipients, key="msg_to_user")
        subject = st.text_input("Subject", key="msg_subject")
        message_body = st.text_area("Message", key="msg_body")
        if st.button("Send", key="msg_send_btn"):
            if to_user and subject and message_body:
                thread_id = f"th_{datetime.now().timestamp()}"
                query("""
                    INSERT INTO messages (sender, recipient, subject, message, timestamp, thread_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (username, to_user, subject, message_body, datetime.now().isoformat(), thread_id), fetch=False)
                st.success("Message sent.")
                st.rerun()
            else:
                st.warning("Fill all fields to send.")

    # Show threads
    if not threads:
        st.info("No messages yet.")
    else:
        for tid, subj, last_time in threads:
            with st.expander(f"{subj} — Last activity {last_time}"):
                msgs = query("""
                    SELECT sender, message, timestamp FROM messages
                    WHERE thread_id=? ORDER BY timestamp ASC
                """, (tid,))
                for s, m, t in msgs:
                    st.markdown(f"**{s}** ({t}):\n> {m}")
                # Reply box
                reply_text = st.text_area(f"Reply to {subj}", key=f"reply_{tid}")
                if st.button(f"Send Reply {tid}", key=f"send_reply_{tid}"):
                    # Enforce only-reply-to-admin for non-admin roles
                    if role != "Admin":
                        if not any(r[0] == "Admin" for r in query("SELECT role FROM users WHERE username=?", (msgs[-1][0],))):
                            st.error("You can only reply to HQ.")
                            continue
                    recipient = msgs[-1][0] if msgs[-1][0] != username else (
                        [u for u in [m[0] for m in msgs] if u != username][-1]
                    )
                    query("""
                        INSERT INTO messages (sender, recipient, subject, message, timestamp, thread_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (username, recipient, subj, reply_text, datetime.now().isoformat(), tid), fetch=False)
                    st.success("Reply sent.")
                    st.rerun()

# --- Shipments Tab ---
if menu == "Shipments":
    st.header("🚚 Shipments")

    # Supplier view — create shipment
    if role == "Supplier":
        st.subheader("Create New Shipment")

        tracking = st.text_input("Tracking Number", key="ship_track")
        carrier = st.text_input("Carrier", key="ship_carrier")
        dest_hub = st.selectbox("Destination Hub", sorted(get_all_hubs()), key="ship_dest")
        ship_date = st.date_input("Shipping Date", key="ship_date")

        skus_in_hub = query("SELECT sku FROM sku_info")
        skus_all = [s[0] for s in skus_in_hub]
        shipment_skus = []
        add_sku = st.selectbox("Select SKU", skus_all, key="ship_sku")
        qty = st.number_input("Quantity", min_value=1, step=1, key="ship_qty")

        if st.button("Add SKU to Shipment", key="ship_addsku"):
            shipment_skus.append((add_sku, qty))
            st.success(f"Added {add_sku} x{qty}")

        if st.button("Submit Shipment", key="ship_submit"):
            if not tracking or not carrier or not dest_hub or not ship_date or not shipment_skus:
                st.warning("Fill all fields and add at least one SKU.")
            else:
                query("""
                    INSERT INTO shipments (supplier, tracking, carrier, hub, date, status)
                    VALUES (?, ?, ?, ?, ?, 'Pending')
                """, (username, tracking, carrier, dest_hub, ship_date.isoformat()), fetch=False)
                ship_id = query("SELECT last_insert_rowid()", fetch=True)[0][0]
                for s, q in shipment_skus:
                    query("INSERT INTO shipment_items (shipment_id, sku, qty) VALUES (?, ?, ?)",
                          (ship_id, s, q), fetch=False)
                st.success("Shipment submitted.")

        # Supplier past shipments
        st.subheader("Your Shipments")
        my_shipments = query("""
            SELECT id, tracking, carrier, hub, date, status
            FROM shipments WHERE supplier=? ORDER BY date DESC
        """, (username,))
        if my_shipments:
            st.dataframe(pd.DataFrame(my_shipments, columns=["ID", "Tracking", "Carrier", "Hub", "Date", "Status"]))
        else:
            st.info("No shipments yet.")

    # Hub Manager / Retail — receive shipment
    elif role in ["Hub Manager", "Retail", "Admin"]:
        st.subheader("Incoming Shipments")
        inc = query("SELECT id, tracking, carrier, date, status FROM shipments WHERE hub=? ORDER BY date DESC",
                    (hub,))
        if not inc:
            st.info("No incoming shipments.")
        else:
            for sid, track, carr, dt, status in inc:
                st.write(f"**Tracking:** {track} | **Carrier:** {carr} | **Date:** {dt} | **Status:** {status}")
                if status == "Pending":
                    if st.button(f"Mark Received {sid}", key=f"recv_{sid}"):
                        # Update inventory
                        items = query("SELECT sku, qty FROM shipment_items WHERE shipment_id=?", (sid,))
                        for sku_code, qty in items:
                            curr = query("SELECT quantity FROM inventory WHERE sku=? AND hub=?", (sku_code, hub))
                            curr_qty = curr[0][0] if curr else 0
                            new_qty = curr_qty + qty
                            query("UPDATE inventory SET quantity=? WHERE sku=? AND hub=?", (new_qty, sku_code, hub), fetch=False)
                            query("INSERT INTO logs VALUES (?, ?, ?, ?, 'IN', ?, ?)",
                                  (datetime.now(), username, sku_code, hub, qty, f"Shipment {sid} received"), fetch=False)
                        query("UPDATE shipments SET status='Received' WHERE id=?", (sid,), fetch=False)
                        st.success("Shipment marked as received and inventory updated.")
                        st.rerun()

        # Shipment history
        st.subheader("Shipment History")
        hist = query("SELECT id, tracking, carrier, hub, date, status FROM shipments ORDER BY date DESC")
        if hist:
            st.dataframe(pd.DataFrame(hist, columns=["ID", "Tracking", "Carrier", "Hub", "Date", "Status"]))
        else:
            st.info("No shipments recorded.")


# ===== Helpers for SKU/Hubs =====
def get_all_hubs():
    return ["Hub 1", "Hub 2", "Hub 3", "Retail"]

def ensure_inventory_row(sku_code: str, hub_name: str):
    # Create row if missing (default 0); never deletes anything
    exists = query("SELECT 1 FROM inventory WHERE sku=? AND hub=?", (sku_code, hub_name))
    if not exists:
        query("INSERT INTO inventory (sku, hub, quantity) VALUES (?, ?, 0)", (sku_code, hub_name), fetch=False)

# --- Create SKU ---
if menu == "Create SKU" and role == "Admin":
    st.header("➕ Create New SKU")

    colA, colB = st.columns([2, 1])
    with colA:
        new_sku = st.text_input("SKU Code", key="create_sku_code").strip()
        product_name = st.text_input("Product Name (optional)", key="create_sku_name").strip()
    with colB:
        hubs_pick = st.multiselect("Assign to Hubs", get_all_hubs(), key="create_sku_hubs")

    if st.button("Create SKU", key="btn_create_sku"):
        if not new_sku:
            st.warning("Enter a SKU code.")
        elif not hubs_pick:
            st.warning("Pick at least one hub.")
        else:
            already = query("SELECT 1 FROM sku_info WHERE sku=?", (new_sku,))
            if already:
                st.warning("SKU already exists.")
            else:
                assigned_str = ",".join(hubs_pick)
                query("INSERT INTO sku_info (sku, product_name, assigned_hubs) VALUES (?, ?, ?)",
                      (new_sku, product_name or new_sku, assigned_str), fetch=False)
                for h in hubs_pick:
                    ensure_inventory_row(new_sku, h)
                st.success(f"✅ Created '{new_sku}' and assigned to: {assigned_str}")

# --- Upload CSV (sku, product_name?, assigned_hubs?) ---
if menu == "Upload CSV" and role == "Admin":
    st.header("📤 Upload SKUs from CSV")
    st.caption("Expected columns: sku, product_name (optional), assigned_hubs (comma-separated, optional).")
    up = st.file_uploader("Choose CSV", type="csv", key="upload_skus_csv")
    if up is not None:
        try:
            df = pd.read_csv(up)
            df.columns = [c.strip().lower() for c in df.columns]
            added, existed = 0, 0
            for _, r in df.iterrows():
                sku = str(r.get("sku", "")).strip()
                if not sku:
                    continue
                prod = str(r.get("product_name", sku)).strip()
                hubs_raw = str(r.get("assigned_hubs", "")).strip()
                hubs_list = [h.strip() for h in hubs_raw.split(",") if h.strip()] or get_all_hubs()  # default: all hubs if omitted?

                if query("SELECT 1 FROM sku_info WHERE sku=?", (sku,)):
                    existed += 1
                    # Merge hubs into assigned_hubs (idempotent)
                    current = query("SELECT assigned_hubs FROM sku_info WHERE sku=?", (sku,))[0][0]
                    cur_set = set([h.strip() for h in (current or "").split(",") if h.strip()])
                    new_set = cur_set.union(hubs_list)
                    merged = ",".join(sorted(new_set))
                    query("UPDATE sku_info SET product_name=?, assigned_hubs=? WHERE sku=?",
                          (prod or sku, merged, sku), fetch=False)
                    for h in new_set:
                        ensure_inventory_row(sku, h)
                else:
                    assigned = ",".join(sorted(set(hubs_list)))
                    query("INSERT INTO sku_info (sku, product_name, assigned_hubs) VALUES (?, ?, ?)",
                          (sku, prod or sku, assigned), fetch=False)
                    for h in hubs_list:
                        ensure_inventory_row(sku, h)
                    added += 1
            st.success(f"✅ Upload complete. Added: {added}, Updated existing: {existed}")
        except Exception as e:
            st.error(f"Upload error: {e}")

# --- Assign SKUs ---
if menu == "Assign SKUs" and role == "Admin":
    st.header("🎯 Assign SKUs to Hubs")

    # Pick SKU
    skus = [s[0] for s in query("SELECT sku FROM sku_info ORDER BY sku")]
    if not skus:
        st.info("No SKUs found. Create one first.")
    else:
        sku_choice = st.selectbox("Select SKU", skus, key="assign_sku_select")

        # Current assignment
        assigned_row = query("SELECT product_name, assigned_hubs FROM sku_info WHERE sku=?", (sku_choice,))
        prod_name = assigned_row[0][0] if assigned_row else ""
        current_hubs = [h for h in (assigned_row[0][1] or "").split(",") if h] if assigned_row else []

        st.write(f"**Product:** {prod_name or sku_choice}")
        new_hubs = st.multiselect("Assign to Hubs", get_all_hubs(), default=current_hubs, key="assign_hubs_multiselect")

        if st.button("Update Assignments", key="btn_update_assignments"):
            # Update assigned_hubs (KISS: do not delete inventory rows even if hub removed)
            assigned_str = ",".join(new_hubs)
            query("UPDATE sku_info SET assigned_hubs=? WHERE sku=?", (assigned_str, sku_choice), fetch=False)
            # Ensure inventory rows exist for any newly added hubs
            for h in new_hubs:
                ensure_inventory_row(sku_choice, h)
            st.success("✅ SKU assignment updated.")

# ===== Manage Users (Admin) =====
def _safe_get_hubs():
    # Reuse existing helper if present
    if "get_all_hubs" in globals():
        return get_all_hubs()
    return ["Hub 1", "Hub 2", "Hub 3", "Retail"]

if menu == "Manage Users" and role == "Admin":
    st.header("🔐 Manage Users")

    # List users
    users_rows = query("SELECT username, role, hub FROM users ORDER BY username")
    users_df = pd.DataFrame(users_rows, columns=["Username", "Role", "Hub"])
    st.dataframe(users_df, use_container_width=True, key="users_table")

    st.markdown("---")
    st.subheader("➕ Create User")

    cu1, cu2, cu3 = st.columns([2, 1, 1])
    with cu1:
        new_username = st.text_input("Username", key="create_user_username").strip()
        new_password = st.text_input("Password", type="password", key="create_user_password")
    with cu2:
        new_role = st.selectbox("Role", ["Admin", "Hub Manager", "Retail", "Supplier"], key="create_user_role")
    with cu3:
        # Hub only for Hub Manager or Retail
        if new_role == "Hub Manager":
            new_hub = st.selectbox("Assign Hub", _safe_get_hubs()[:-1], key="create_user_hub_mgr")  # exclude 'Retail'
        elif new_role == "Retail":
            new_hub = "Retail"
            st.write("Hub: Retail")
        else:
            new_hub = ""  # Admin / Supplier: no hub

    if st.button("Create User", key="btn_create_user"):
        if not new_username or not new_password:
            st.warning("Please enter both username and password.")
        else:
            exists = query("SELECT 1 FROM users WHERE username=?", (new_username,))
            if exists:
                st.warning("User already exists.")
            else:
                query(
                    "INSERT INTO users (username, password, role, hub) VALUES (?, ?, ?, ?)",
                    (new_username, hash_pw(new_password), new_role, new_hub),
                    fetch=False
                )
                st.success(f"✅ User '{new_username}' created.")

    st.markdown("---")
    st.subheader("🗑️ Remove User")

    # Prevent deleting yourself; keep it simple
    other_users = [u[0] for u in users_rows if u[0] != username]
    if not other_users:
        st.info("No other users to remove.")
    else:
        del_user = st.selectbox("Select user to remove", other_users, key="remove_user_select")
        confirm_txt = st.text_input(f"Type the username '{del_user}' to confirm", key="remove_user_confirm_input")
        if st.button("Remove User", key="btn_remove_user"):
            if confirm_txt.strip() == del_user:
                query("DELETE FROM users WHERE username=?", (del_user,), fetch=False)
                st.success(f"✅ Removed '{del_user}'.")
            else:
                st.warning("Confirmation text did not match. User not removed.")

# ===== Backup / Snapshots (Admin) =====
import os, shutil

# Ensure snapshot dir exists (idempotent)
if "SNAP_DIR" not in globals():
    APP_DIR = Path(__file__).parent
    DB = APP_DIR / "ttt_inventory.db" if "DB" not in globals() else DB
    SNAP_DIR = APP_DIR / "snapshots"
    SNAP_DIR.mkdir(exist_ok=True)

def snapshot_db(label: str = "") -> Path | None:
    """Copy DB to snapshots/ with timestamp + optional label."""
    if not DB.exists():
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"-{label.strip().replace(' ', '_')}" if label else ""
    out = SNAP_DIR / f"ttt_inventory_{ts}{suffix}.db"
    shutil.copy2(DB, out)
    return out

def list_snapshots() -> list[Path]:
    return sorted(SNAP_DIR.glob("ttt_inventory_*.db"))

def restore_db(snapshot_path: Path) -> bool:
    if snapshot_path and snapshot_path.exists():
        shutil.copy2(snapshot_path, DB)
        return True
    return False

if menu == "Backup" and role == "Admin":
    st.header("🗄️ Database Snapshots")

    # Take snapshot
    colA, colB = st.columns([3, 1])
    with colA:
        snap_label = st.text_input("Optional label for snapshot", key="snap_label")
    with colB:
        if st.button("📸 Take Snapshot", key="btn_take_snapshot"):
            out = snapshot_db(snap_label)
            if out:
                st.success(f"✅ Snapshot saved: `{out.name}`")
            else:
                st.warning("No database file found to snapshot.")

    st.markdown("---")
    st.subheader("🔁 Restore from Snapshot")

    snaps = list_snapshots()
    if not snaps:
        st.info("No snapshots found yet. Create one above.")
    else:
        snap_names = [p.name for p in snaps]
        pick = st.selectbox("Choose snapshot", snap_names, key="restore_pick")
        if st.button("Restore Selected Snapshot", key="btn_restore_snapshot"):
            ok = restore_db(SNAP_DIR / pick)
            if ok:
                st.success(f"✅ Restored from `{pick}`. Reload the app to see all changes.")
            else:
                st.error("Restore failed. File not found or unreadable.")

    st.markdown("---")
    st.subheader("☁️ Upload Snapshot to Restore")

    up_snap = st.file_uploader("Upload a .db snapshot to restore", type=["db"], key="upload_snapshot")
    if up_snap is not None:
        # Save upload to a temp file inside snapshots then restore
        temp_path = SNAP_DIR / f"uploaded_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        with open(temp_path, "wb") as f:
            f.write(up_snap.read())
        st.success(f"✅ Uploaded snapshot: `{temp_path.name}`")
        if st.button("Restore Uploaded Snapshot", key="btn_restore_uploaded"):
            ok = restore_db(temp_path)
            if ok:
                st.success("✅ Restored from uploaded snapshot. Reload the app to see all changes.")
            else:
                st.error("Restore failed from uploaded snapshot.")


# ===== Helpers =====
def get_all_hubs() -> list[str]:
    # Keep hub names in one place
    return ["Hub 1", "Hub 2", "Hub 3", "Retail"]

def is_sku_assigned_to_hub(sku: str, hub_name: str) -> bool:
    row = query("SELECT assigned_hubs FROM sku_info WHERE sku=?", (sku,))
    if not row:
        return False
    hubs_csv = row[0][0] or ""
    hubs = [h.strip() for h in hubs_csv.split(",") if h.strip()]
    return hub_name in hubs

def ensure_inventory_row(sku: str, hub_name: str):
    # Create inventory row if missing
    exists = query("SELECT 1 FROM inventory WHERE sku=? AND hub=?", (sku, hub_name))
    if not exists:
        query("INSERT OR IGNORE INTO inventory (sku, hub, quantity) VALUES (?, ?, ?)", (sku, hub_name, 0), fetch=False)

# ===== Inventory =====
if menu == "Inventory":
    st.header("📦 Inventory")

    view_hub = hub if role != "Admin" else st.selectbox(
        "Select Hub", get_all_hubs(), index=0, key="inv_hub_select"
    )
    search_txt = st.text_input("Search (SKU or Product Name)", key="inv_search_txt")

    inv_rows = query("SELECT sku, quantity FROM inventory WHERE hub = ? ORDER BY sku", (view_hub,))
    name_map = dict(query("SELECT sku, product_name FROM sku_info"))

    display_rows = []
    for s, q in inv_rows:
        pname = name_map.get(s, "")
        if search_txt:
            t = search_txt.lower()
            if t not in s.lower() and t not in pname.lower():
                continue
        display_rows.append((s, pname, q))

    df_inv = pd.DataFrame(display_rows, columns=["SKU", "Product Name", "Qty"])
    st.dataframe(df_inv, use_container_width=True, key="inv_table")

    # Quick export
    inv_csv = df_inv.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Inventory CSV", inv_csv, "inventory.csv", "text/csv", key="inv_dl")

# ===== Update Stock =====
if menu == "Update Stock":
    st.header("🔁 Update Inventory")

    upd_hub = hub if role != "Admin" else st.selectbox(
        "Select Hub", get_all_hubs(), key="upd_hub_select"
    )

    sku_name_pairs = query("SELECT sku, product_name FROM sku_info ORDER BY sku")
    # Filter by assigned-to-hub
    available = [s for s, _ in sku_name_pairs if is_sku_assigned_to_hub(s, upd_hub)]
    label_map = {s: f"{s} — {dict(sku_name_pairs).get(s,'')}" for s in available}

    if not available:
        st.info("No SKUs assigned to this hub yet.")
    else:
        pick = st.selectbox("Select SKU", available, format_func=lambda x: label_map[x], key="upd_sku_select")
        action = st.radio("Action", ["IN", "OUT"], horizontal=True, key="upd_action_radio")
        qty = st.number_input("Quantity", min_value=1, step=1, key="upd_qty_input")
        comment = st.text_input("Optional Comment", key="upd_comment_input")

        if st.button("Submit Update", key="upd_submit_btn"):
            ensure_inventory_row(pick, upd_hub)
            cur = query("SELECT quantity FROM inventory WHERE sku=? AND hub=?", (pick, upd_hub))
            current = cur[0][0] if cur else 0
            new_qty = current + qty if action == "IN" else current - qty
            if new_qty < 0:
                st.warning("❌ Not enough stock to remove.")
            else:
                query("UPDATE inventory SET quantity=? WHERE sku=? AND hub=?", (new_qty, pick, upd_hub), fetch=False)
                query(
                    "INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (datetime.now().isoformat(), username, pick, upd_hub, action, qty, comment),
                    fetch=False
                )
                st.success(f"✅ {action} {qty} for {pick}. New Qty: {new_qty}")

# ===== Bulk Update =====
if menu == "Bulk Update":
    st.header("📝 Bulk Inventory Update")

    bulk_hub = hub if role != "Admin" else st.selectbox(
        "Select Hub", get_all_hubs(), key="bulk_hub_select"
    )
    rows = query("SELECT sku, quantity FROM inventory WHERE hub=? ORDER BY sku", (bulk_hub,))
    df_bulk = pd.DataFrame(rows, columns=["SKU", "Current Qty"])

    if df_bulk.empty:
        st.info("No inventory rows for this hub yet.")
    else:
        st.info("Enter a positive number for IN, negative for OUT. Leave blank to skip.")
        edits = {}
        for i, r in df_bulk.iterrows():
            with st.expander(f"{r['SKU']} (Current: {r['Current Qty']})", expanded=False):
                adj = st.text_input("Adjust (+IN / -OUT)", "", key=f"bulk_adj_{i}")
                cmt = st.text_input("Comment (optional)", "", key=f"bulk_cmt_{i}")
                edits[r["SKU"]] = (adj, cmt)

        if st.button("Apply All Updates", key="bulk_apply_btn"):
            errs, oks = [], []
            for s, (adj, cmt) in edits.items():
                adj = (adj or "").strip()
                if not adj:
                    continue
                try:
                    n = int(adj)
                except:
                    errs.append(f"{s}: invalid number '{adj}'")
                    continue
                # ensure row
                ensure_inventory_row(s, bulk_hub)
                cur = query("SELECT quantity FROM inventory WHERE sku=? AND hub=?", (s, bulk_hub))
                current = cur[0][0] if cur else 0
                new_qty = current + n
                if new_qty < 0:
                    errs.append(f"{s}: not enough stock (have {current}, tried {n})")
                    continue
                action = "IN" if n > 0 else "OUT"
                query("UPDATE inventory SET quantity=? WHERE sku=? AND hub=?", (new_qty, s, bulk_hub), fetch=False)
                query(
                    "INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (datetime.now().isoformat(), username, s, bulk_hub, action, abs(n), cmt),
                    fetch=False
                )
                oks.append(f"{s}: {action} {abs(n)} (Now {new_qty})")

            if errs:
                st.warning("Some updates failed:\n- " + "\n- ".join(errs))
            if oks:
                st.success("✅ Bulk update complete:\n- " + "\n- ".join(oks))

# ===== Logs =====
if menu == "Logs":
    st.header("📜 Activity Logs")

    rows = query("SELECT * FROM logs ORDER BY timestamp DESC")
    df_logs = pd.DataFrame(rows, columns=["Time", "User", "SKU", "Hub", "Action", "Qty", "Comment"])

    if df_logs.empty:
        st.info("No logs yet.")
    else:
        df_logs["Time"] = pd.to_datetime(df_logs["Time"]).dt.strftime("%Y-%m-%d %H:%M")

        with st.expander("🔎 Filters"):
            c1, c2, c3, c4 = st.columns(4)
            user_f = c1.selectbox("User", ["All"] + sorted(df_logs["User"].unique()), key="log_user_f")
            hub_f = c2.selectbox("Hub", ["All"] + get_all_hubs(), key="log_hub_f")
            action_f = c3.selectbox("Action", ["All", "IN", "OUT"], key="log_action_f")
            sku_f = c4.text_input("SKU contains", key="log_sku_f")

        view = df_logs.copy()
        if role != "Admin":
            view = view[view["Hub"] == hub]
        if user_f != "All":
            view = view[view["User"] == user_f]
        if hub_f != "All":
            view = view[view["Hub"] == hub_f]
        if action_f != "All":
            view = view[view["Action"] == action_f]
        if sku_f:
            view = view[view["SKU"].str.contains(sku_f, case=False, na=False)]

        st.dataframe(view, use_container_width=True, key="logs_table")

        buff = io.BytesIO()
        view.to_csv(buff, index=False)
        st.download_button("📥 Download CSV", buff.getvalue(), "logs.csv", "text/csv", key="logs_dl_btn")

# ===== Messages =====
if menu == "Messages":
    st.header("💬 Internal Messages")

    # Choose recipient
    if role == "Admin":
        recipients = [r[0] for r in query("SELECT username FROM users WHERE username != ?", (username,))]
    else:
        recipients = [r[0] for r in query("SELECT username FROM users WHERE role='Admin'")]
    if not recipients:
        st.info("No recipients available.")
    else:
        to_user = st.selectbox("To", recipients, key="msg_to")
        subject = st.text_input("Subject", key="msg_subject")
        body = st.text_area("Message", key="msg_body")
        if st.button("Send", key="msg_send_btn"):
            thread_id = subject.strip() if subject.strip() else f"{username}-{to_user}"
            query(
                "INSERT INTO messages (sender, recipient, subject, message, timestamp, thread_id, reply_to) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (username, to_user, subject, body, datetime.now().isoformat(), thread_id, None),
                fetch=False
            )
            st.success("✅ Message sent.")

    st.subheader("📨 Your Threads")
    threads = query("SELECT DISTINCT thread_id FROM messages WHERE sender=? OR recipient=? ORDER BY timestamp DESC", (username, username))
    for (tid,) in threads:
        msgs = query("SELECT id, timestamp, sender, subject, message FROM messages WHERE thread_id=? ORDER BY timestamp", (tid,))
        with st.expander(f"🧵 {tid}"):
            for mid, ts, snd, sub, msg in msgs:
                st.markdown(f"**{snd}** — {ts}")
                if sub:
                    st.markdown(f"**Subject:** {sub}")
                st.write(msg)
                st.markdown("---")
            reply = st.text_area("Reply", key=f"reply_body_{tid}")
            if st.button("Send Reply", key=f"reply_btn_{tid}"):
                # Reply goes to the other participant (simple)
                last_from_other = [m[2] for m in msgs if m[2] != username]
                to = last_from_other[-1] if last_from_other else (recipients[0] if recipients else username)
                query(
                    "INSERT INTO messages (sender, recipient, subject, message, timestamp, thread_id, reply_to) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (username, to, f"Re: {tid}", reply, datetime.now().isoformat(), tid, msgs[-1][0] if msgs else None),
                    fetch=False
                )
                st.success("✅ Reply sent.")


# ===== Shipments =====
if menu == "Shipments":
    st.header("🚚 Shipments")

    if role == "Supplier":
        st.subheader("📝 Create Shipment")
        trk = st.text_input("Tracking #", key="ship_trk")
        car = st.text_input("Carrier", key="ship_car")
        dest = st.selectbox("Destination Hub", get_all_hubs(), key="ship_dest")
        sdate = st.date_input("Shipping Date", key="ship_date")

        # Add items
        if "ship_items" not in st.session_state:
            st.session_state["ship_items"] = []
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            si_sku = st.text_input("SKU", key="ship_item_sku")
        with c2:
            si_qty = st.number_input("Qty", min_value=1, step=1, key="ship_item_qty")
        with c3:
            if st.button("➕ Add Item", key="ship_add_item"):
                if si_sku.strip():
                    st.session_state["ship_items"].append((si_sku.strip(), int(si_qty)))

        if st.session_state["ship_items"]:
            st.markdown("**Items:**")
            for i, (s, q) in enumerate(st.session_state["ship_items"]):
                st.write(f"• {s} — {q}")
                if st.button(f"Remove {s}", key=f"ship_rm_{i}"):
                    st.session_state["ship_items"].pop(i)

        if st.button("Submit Shipment", key="ship_submit_btn"):
            if trk and car and dest and sdate and st.session_state["ship_items"]:
                query("INSERT INTO shipments (supplier, tracking, carrier, hub, date, status) VALUES (?, ?, ?, ?, ?, 'Pending')",
                      (username, trk, car, dest, str(sdate)), fetch=False)
                ship_id = query("SELECT last_insert_rowid()")[0][0]
                for s, q in st.session_state["ship_items"]:
                    query("INSERT INTO shipment_items (shipment_id, sku, qty) VALUES (?, ?, ?)", (ship_id, s, q), fetch=False)
                st.success("✅ Shipment submitted.")
                st.session_state["ship_items"] = []
            else:
                st.warning("Fill out all fields and add at least one item.")

        st.subheader("📦 Your Shipments")
        mine = query("SELECT id, tracking, carrier, hub, date, status FROM shipments WHERE supplier=? ORDER BY id DESC", (username,))
        if not mine:
            st.info("No shipments yet.")
        else:
            for sid, tr, cr, hb, dt, stt in mine:
                with st.expander(f"{tr} | {cr} → {hb} on {dt} | {stt}"):
                    items = query("SELECT sku, qty FROM shipment_items WHERE shipment_id=?", (sid,))
                    for s, q in items:
                        st.write(f"• {s}: {q}")

    else:
        st.subheader("📥 Pending Shipments")
        rows = query("SELECT id, supplier, tracking, carrier, hub, date, status FROM shipments WHERE status='Pending' ORDER BY id DESC")
        if not rows:
            st.info("No pending shipments.")
        else:
            pick_id = st.selectbox("Select pending shipment to receive", [r[0] for r in rows], key="ship_recv_pick")
            if pick_id:
                hdr = [r for r in rows if r[0] == pick_id][0]
                sid, sup, tr, cr, hb, dt, stt = hdr
                st.write(f"**{tr}** — {cr} → {hb} on {dt}")
                items = query("SELECT sku, qty FROM shipment_items WHERE shipment_id=?", (sid,))
                for s, q in items:
                    st.write(f"• {s}: {q}")
                if st.button("Mark Received", key="ship_mark_received_btn"):
                    # Apply to inventory
                    for s, q in items:
                        ensure_inventory_row(s, hb)
                        cur = query("SELECT quantity FROM inventory WHERE sku=? AND hub=?", (s, hb))
                        current = cur[0][0] if cur else 0
                        new_qty = current + int(q)
                        query("UPDATE inventory SET quantity=? WHERE sku=? AND hub=?", (new_qty, s, hb), fetch=False)
                        query(
                            "INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (datetime.now().isoformat(), username, s, hb, "IN", int(q), f"Shipment {sid}"),
                            fetch=False
                        )
                    query("UPDATE shipments SET status='Received' WHERE id=?", (sid,), fetch=False)
                    st.success("✅ Shipment received and inventory updated.")

        if role == "Admin":
            st.markdown("---")
            st.subheader("🗑️ Delete Shipment")
            all_not_deleted = query("SELECT id, tracking FROM shipments WHERE status!='Deleted' ORDER BY id DESC")
            if all_not_deleted:
                del_id = st.selectbox("Pick shipment to delete", [i for i, _ in all_not_deleted], key="ship_del_id")
                if st.button("Delete Shipment", key="ship_del_btn"):
                    query("UPDATE shipments SET status='Deleted' WHERE id=?", (del_id,), fetch=False)
                    st.success("✅ Shipment deleted.")
            else:
                st.info("No shipments to delete.")

# ===== Assign SKUs (Admin) =====
if menu == "Assign SKUs" and role == "Admin":
    st.header("🎯 Assign SKUs to Hubs")

    skus = [s for (s,) in query("SELECT sku FROM sku_info ORDER BY sku")]
    if not skus:
        st.info("No SKUs yet. Create one first.")
    else:
        sku_pick = st.selectbox("Select SKU", skus, key="assign_sku_pick")

        assigned_csv = query("SELECT assigned_hubs FROM sku_info WHERE sku=?", (sku_pick,))
        current = (assigned_csv[0][0] or "").split(",") if assigned_csv else []
        current = [c.strip() for c in current if c.strip()]

        hubs = get_all_hubs()
        new_assign = st.multiselect("Assign to Hubs", hubs, default=current, key="assign_hubs_ms")

        if st.button("Update Assignments", key="assign_update_btn"):
            combined = ",".join(new_assign)
            query("UPDATE sku_info SET assigned_hubs=? WHERE sku=?", (combined, sku_pick), fetch=False)

            # ✅ Ensure inventory rows exist for all newly assigned hubs
            for h in new_assign:
                ensure_inventory_row(sku_pick, h)

            # (Optional) If you want to remove inventory rows for unassigned hubs, do it explicitly:
            # for h in (set(hubs) - set(new_assign)):
            #     query("DELETE FROM inventory WHERE sku=? AND hub=?", (sku_pick, h), fetch=False)

            st.success("✅ Assignment updated and inventory rows ensured.")

# ===== Create SKU (Admin) =====
if menu == "Create SKU" and role == "Admin":
    st.header("➕ Create New SKU")

    new_sku = st.text_input("SKU Code", key="create_sku_code").strip()
    prod_name = st.text_input("Product Name", key="create_sku_name").strip()
    hubs_ms = st.multiselect("Assign to Hubs", get_all_hubs(), key="create_sku_hubs")

    if st.button("Create SKU", key="create_sku_btn"):
        if not new_sku:
            st.warning("Enter a SKU code.")
        elif not prod_name:
            st.warning("Enter a product name.")
        elif not hubs_ms:
            st.warning("Assign at least one hub.")
        else:
            exist = query("SELECT 1 FROM sku_info WHERE sku=?", (new_sku,))
            if exist:
                st.warning("SKU already exists.")
            else:
                query("INSERT INTO sku_info (sku, product_name, assigned_hubs) VALUES (?, ?, ?)",
                      (new_sku, prod_name, ",".join(hubs_ms)), fetch=False)
                # Ensure inventory rows exist
                for h in hubs_ms:
                    ensure_inventory_row(new_sku, h)
                st.success(f"✅ Created SKU '{new_sku}' and assigned to {', '.join(hubs_ms)}.")

# ===== Upload CSV (Admin) =====
# CSV columns expected: sku, product_name, assigned_hubs (comma-separated)
if menu == "Upload CSV" and role == "Admin":
    st.header("⬆️ Upload SKUs from CSV")

    up = st.file_uploader("Choose CSV", type=["csv"], key="upload_sku_csv")
    if up is not None:
        try:
            df = pd.read_csv(up)
            if df.empty:
                st.warning("CSV is empty.")
            else:
                cnt = 0
                for _, row in df.iterrows():
                    sku = str(row.get("sku", "")).strip()
                    pname = str(row.get("product_name", sku)).strip()
                    hubs_csv = str(row.get("assigned_hubs", "")).strip()
                    hubs_list = [h.strip() for h in hubs_csv.split(",") if h.strip()]

                    if not sku:
                        continue
                    # upsert sku_info
                    exists = query("SELECT 1 FROM sku_info WHERE sku=?", (sku,))
                    if exists:
                        query("UPDATE sku_info SET product_name=?, assigned_hubs=? WHERE sku=?",
                              (pname, ",".join(hubs_list), sku), fetch=False)
                    else:
                        query("INSERT INTO sku_info (sku, product_name, assigned_hubs) VALUES (?, ?, ?)",
                              (sku, pname, ",".join(hubs_list)), fetch=False)
                    # ensure inventory rows
                    for h in hubs_list:
                        ensure_inventory_row(sku, h)
                    cnt += 1
                st.success(f"✅ Processed {cnt} rows.")
        except Exception as e:
            st.error(f"Upload error: {e}")

# ===== Inventory Count =====
if menu == "Inventory Count":
    st.header("🧾 Inventory Count Mode")

    if role != "Admin":
        # count one sku at a time (KISS)
        skus_here = [s for (s,) in query("SELECT sku FROM sku_info ORDER BY sku") if is_sku_assigned_to_hub(s, hub)]
        if not skus_here:
            st.info("No SKUs assigned to your hub.")
        else:
            csku = st.selectbox("Select SKU", skus_here, key="count_sku_pick")
            counted = st.number_input("Counted Quantity", min_value=0, step=1, key="count_qty_input")
            if st.button("✅ Confirm Count", key="count_confirm_btn"):
                query(
                    "INSERT INTO count_confirmations (sku, hub, count, confirmed_by, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (csku, hub, int(counted), username, datetime.now().isoformat()),
                    fetch=False
                )
                st.success("✅ Count recorded.")

    else:
        st.subheader("Confirmed Counts")
        dfc = pd.DataFrame(
            query("SELECT sku, hub, count, confirmed_by, timestamp FROM count_confirmations ORDER BY timestamp DESC"),
            columns=["SKU", "Hub", "Count", "Confirmed By", "Time"]
        )
        if dfc.empty:
            st.info("No confirmations yet.")
        else:
            st.dataframe(dfc, use_container_width=True, key="count_confirm_table")
            buff = io.BytesIO()
            dfc.to_csv(buff, index=False)
            st.download_button("📥 Download Confirmations CSV", buff.getvalue(), "confirmations.csv", "text/csv", key="count_dl_btn")

# ===== Google Sheets (optional) =====
if menu == "Google Sheets" and role in ["Admin", "Hub Manager", "Retail"]:
    st.header("📊 Google Sheets Inventory Reference")
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSg2Hyk9x4Uaz2kkBh2PkoKJlnpth6evjHKX9m0FfuxXK28c6HSWYpTaYjYCzI2f5Y0bKm6YUhSCoa9/pubhtml?gid=1829911536&single=true"
    st.markdown(f'<iframe src="{sheet_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
    st.markdown(f"[Open Google Sheets in new tab]({sheet_url})")

