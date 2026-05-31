

 #-libary set up /database/ manage file data
import sqlite3, os, re
from datetime import date, datetime, timedelta
#- terminal color section
class C:
    R='\033[91m'; G='\033[92m'; Y='\033[93m'; B='\033[94m'
    CY='\033[96m'; M='\033[95m'; BO='\033[1m'; E='\033[0m'
#-database name
DB = 'pro_gym.db'
conn = lambda: sqlite3.connect(DB)

# ── DB SETUP ──────────────────────────────────────────────
def setup_database():     
    with conn() as c:
        cur = c.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS trainers(
                                                              t_id INTEGER PRIMARY KEY AUTOINCREMENT, t_name TEXT NOT NULL, expertise TEXT)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS members(
                                                             m_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER,
                                                             dob DATE, email TEXT, contact TEXT, bmi_status TEXT, plan TEXT, diet TEXT,
                                                             t_id INTEGER, join_date DATE, expiry_date DATE,
                                                             FOREIGN KEY(t_id) REFERENCES trainers(t_id))''')
        cur.execute("PRAGMA table_info(members)")
        cols = [r[1] for r in cur.fetchall()]
        for col, typ in [('dob','DATE'),('email','TEXT'),('contact','TEXT')]:
            if col not in cols:
                cur.execute(f"ALTER TABLE members ADD COLUMN {col} {typ}")
                print(f"{C.Y}⚙️  Migration: '{col}' added.{C.E}")
        cur.execute('SELECT COUNT(*) FROM trainers')
        if cur.fetchone()[0] == 0:
            cur.executemany('INSERT INTO trainers(t_name,expertise) VALUES(?,?)',
                            [('Raju Bhai','Bodybuilding'),('Priya Roy','Weight Loss'),('Vikram','CrossFit'),( "Athlean-X",'Science-based Muscle Building'   )])

# ── VALIDATORS ────────────────────────────────────────────
def get_int(p, mn=None, mx=None):
    while True:
        try:
            v = int(input(p))
            if mn is not None and v < mn: print(f"{C.R} Min {mn}.{C.E}"); continue
            if mx is not None and v > mx: print(f"{C.R} Max {mx}.{C.E}"); continue
            return v
        except ValueError: print(f"{C.R} Number din.{C.E}")

def get_float(p, mn=0.1):
    while True:
        try:
            v = float(input(p))
            if v >= mn: return v
            print(f"{C.R} {mn}+ hobe.{C.E}")
        except ValueError: print(f"{C.R} Decimal din.{C.E}")

def get_non_empty(p):
    while True:
        v = input(p).strip()
        if v: return v
        print(f"{C.R} not empty.{C.E}")

def get_email(p):
    pat = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while True:
        v = input(p).strip()
        if re.match(pat, v): return v.lower()
        print(f"{C.R} Valid email enter.{C.E}")

def get_contact(p):
    while True:
        v = input(p).strip().replace(' ','').replace('-','')
        v = v[3:] if v.startswith('+91') else (v[1:] if v.startswith('0') else v)
        if v.isdigit() and len(v)==10: return v
        print(f"{C.R} 10-digit number din.{C.E}")

def get_dob(p):
    while True:
        v = input(p).strip()
        try:
            dob = datetime.strptime(v,'%Y-%m-%d').date()
            if dob >= date.today(): print(f"{C.R} Past date hobe.{C.E}"); continue
            a = calc_age(dob)
            if not 10 <= a <= 100: print(f"{C.R} Age 10-100 (got {a}).{C.E}"); continue
            return dob
        except ValueError: print(f"{C.R} Format: YYYY-MM-DD{C.E}")

def calc_age(dob):
    t = date.today()
    return t.year - dob.year - ((t.month,t.day) < (dob.month,dob.day))

# ── BMI ───────────────────────────────────────────────────
def calc_bmi(w, h):
    b = round(w / (h/100)**2, 2)
    cat = "Underweight" if b<18.5 else "Normal" if b<25 else "Overweight" if b<30 else "Obese"
    return b, cat

# ── TRAINERS ──────────────────────────────────────────────
def show_trainers():
    with conn() as c:
        rows = c.execute('SELECT t_id,t_name,expertise FROM trainers').fetchall()
    print(f"\n{C.CY}Available Trainers:{C.E}")
    for r in rows: print(f"  {C.Y}{r[0]}{C.E} - {r[1]} ({r[2]})")
    return [r[0] for r in rows]

# ── CRUD ──────────────────────────────────────────────────
def add_member():
    print(f"\n{C.BO}{C.CY}--- ADD NEW MEMBER ---{C.E}")
    name = get_non_empty("Name: ")
    dob  = get_dob("DOB (YYYY-MM-DD): ")
    age  = calc_age(dob)
    print(f"{C.G} Age: {age}{C.E}")
    email   = get_email("Email: ")
    contact = get_contact("Contact (10-digit): ")

    with conn() as c:
        ex = c.execute("SELECT name FROM members WHERE email=? OR contact=?",(email,contact)).fetchone()
        if ex: print(f"{C.R} '{ex[0]}' already registered!{C.E}"); return

    w,h = get_float("Weight (kg): "), get_float("Height (cm): ")
    bmi, bmi_s = calc_bmi(w, h)
    print(f"{C.G} BMI: {bmi} | {bmi_s}{C.E}")
    months = get_int("Plan duration (1-12 months): ", 1, 12)
    diet   = get_non_empty("Diet (Weight Loss/Muscle Gain/Keto): ")
    valid  = show_trainers()
    while True:
        tid = get_int("Trainer ID: ")
        if tid in valid: break
        print(f"{C.R} Invalid ID.{C.E}")
    jd = date.today(); ed = jd + timedelta(days=30*months)
    with conn() as c:
        c.execute('''INSERT INTO members(name,age,dob,email,contact,bmi_status,plan,diet,t_id,join_date,expiry_date)
                     VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                  (name,age,dob.isoformat(),email,contact,bmi_s,f"{months} Months",diet,tid,jd.isoformat(),ed.isoformat()))
    print(f"\n{C.G} '{name}' joined! Expiry: {ed}{C.E}")

def view_all_with_trainers():
    with conn() as c:
        rows = c.execute('''SELECT m.m_id,m.name,m.age,m.contact,m.plan,m.expiry_date,t.t_name
                            FROM members m INNER JOIN trainers t ON m.t_id=t.t_id ORDER BY m.m_id''').fetchall()
    if not rows: print(f"\n{C.Y} No members.{C.E}"); return
    print(f"\n{C.CY}{'='*100}{C.E}")
    print(f"{C.BO}{C.CY}                          GYM MEMBER DETAILS{C.E}")
    print(f"{C.CY}{'='*100}{C.E}")
    print(f"{C.BO}{'ID':<4} | {'NAME':<15} | {'AGE':<4} | {'CONTACT':<12} | {'PLAN':<10} | {'EXPIRY':<12} | {'TRAINER':<15}{C.E}")
    print("-"*100)
    today = date.today()
    for r in rows:
        try:
            ex = date.fromisoformat(r[5])
            ec = C.R if ex<today else (C.Y if (ex-today).days<=7 else C.G)
            es = f"{ec}{r[5]:<12}{C.E}"
        except: es = f"{'N/A':<12}"
        print(f"{r[0]:<4} | {r[1]:<15} | {str(r[2]):<4} | {(r[3] or 'N/A'):<12} | {r[4]:<10} | {es} | {r[6]:<15}")
    print(f"{C.CY}{'='*100}{C.E}")

def search_member():
    print(f"\n{C.BO}{C.CY}--- SEARCH MEMBER ---{C.E}")
    kw = get_non_empty("Name / Email / Contact: ")
    with conn() as c:
        rows = c.execute('''SELECT m.m_id,m.name,m.age,m.dob,m.email,m.contact,m.bmi_status,
                                   m.plan,m.diet,m.join_date,m.expiry_date,t.t_name
                            FROM members m LEFT JOIN trainers t ON m.t_id=t.t_id
                            WHERE m.name LIKE ? OR m.email LIKE ? OR m.contact LIKE ?''',
                         (f'%{kw}%',)*3).fetchall()
    if not rows: print(f"{C.R} Not found.{C.E}"); return
    labels = ["ID","Name","Age","DOB","Email","Contact","BMI","Plan","Diet","Joined","Expiry","Trainer"]
    for r in rows:
        print(f"\n{C.G}{'━'*35}{C.E}")
        for l,v in zip(labels,r): print(f"  {l:<9}: {v or 'N/A'}")

def update_member():
    print(f"\n{C.BO}{C.CY}--- UPDATE MEMBER ---{C.E}")
    mid = get_int("Member ID: ")
    with conn() as c:
        cur = c.cursor()
        m = cur.execute("SELECT name,email,contact,plan,diet FROM members WHERE m_id=?",(mid,)).fetchone()
        if not m: print(f"{C.R} ID {mid} not found.{C.E}"); return
        print(f"Current -> Name:{m[0]}  Email:{m[1] or 'N/A'}  Contact:{m[2] or 'N/A'}  Plan:{m[3]}  Diet:{m[4]}")
        print(f"{C.Y}(Blank = keep old value){C.E}")
        ne = input("New Email: ").strip()
        nc = input("New Contact: ").strip()
        nd = input("New Diet: ").strip()
        ex = input("Extend plan (months, 0=skip): ").strip()
        if ne:
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', ne):
                cur.execute("UPDATE members SET email=? WHERE m_id=?",(ne.lower(),mid))
            else: print(f"{C.R} Invalid email, skipped.{C.E}")
        if nc:
            nc = nc.replace(' ','').replace('-','').lstrip('+91').lstrip('0')
            if nc.isdigit() and len(nc)==10: cur.execute("UPDATE members SET contact=? WHERE m_id=?",(nc,mid))
            else: print(f"{C.R} Invalid contact, skipped.{C.E}")
        if nd: cur.execute("UPDATE members SET diet=? WHERE m_id=?",(nd,mid))
        if ex and ex!='0':
            try:
                ed = date.fromisoformat(cur.execute("SELECT expiry_date FROM members WHERE m_id=?",(mid,)).fetchone()[0])
                ned = ed + timedelta(days=30*int(ex))
                cur.execute("UPDATE members SET expiry_date=? WHERE m_id=?",(ned.isoformat(),mid))
                print(f"{C.G} New expiry: {ned}{C.E}")
            except ValueError: print(f"{C.R} Invalid months, skipped.{C.E}")
    print(f"{C.G} Updated!{C.E}")

def delete_member():
    print(f"\n{C.BO}{C.CY}--- DELETE MEMBER ---{C.E}")
    mid = get_int("Member ID: ")
    with conn() as c:
        cur = c.cursor()
        m = cur.execute("SELECT name FROM members WHERE m_id=?",(mid,)).fetchone()
        if not m: print(f"{C.R} ID {mid} not found.{C.E}"); return
        if input(f"{C.Y}Delete '{m[0]}'? (y/n): {C.E}").lower()=='y':
            cur.execute("DELETE FROM members WHERE m_id=?",(mid,))
            print(f"{C.G}✅ '{m[0]}' deleted.{C.E}")
        else: print(f"{C.Y} Cancelled.{C.E}")

def expiring_soon():
    print(f"\n{C.BO}{C.CY}--- EXPIRING SOON (Next 7 Days) ---{C.E}")
    today = date.today(); wl = today + timedelta(days=7)
    with conn() as c:
        rows = c.execute('''SELECT m_id,name,contact,expiry_date FROM members
                            WHERE expiry_date BETWEEN ? AND ? ORDER BY expiry_date''',
                         (today.isoformat(),wl.isoformat())).fetchall()
    if not rows: print(f"{C.G}✅ No expiries next 7 days.{C.E}"); return
    for r in rows:
        dl = (date.fromisoformat(r[3])-today).days
        print(f"  {C.Y}ID {r[0]}: {r[1]} ({r[2] or 'N/A'}) -> {r[3]} ({dl} days){C.E}")

def birthdays_this_month():
    print(f"\n{C.BO}{C.CY}--- BIRTHDAYS THIS MONTH ---{C.E}")
    with conn() as c:
        rows = c.execute('''SELECT m_id,name,dob,contact FROM members
                            WHERE dob IS NOT NULL AND CAST(strftime('%m',dob) AS INTEGER)=?
                            ORDER BY CAST(strftime('%d',dob) AS INTEGER)''',
                         (date.today().month,)).fetchall()
    if not rows: print(f"{C.Y} No birthdays this month.{C.E}"); return
    for r in rows:
        print(f"  {C.M}🎂 ID {r[0]}: {r[1]} - {date.fromisoformat(r[2]).strftime('%d %B')} ({r[3] or 'N/A'}){C.E}")

# ── MAIN ──────────────────────────────────────────────────
def main():
    setup_database()
    menu = {
        '1':add_member, '2':view_all_with_trainers, '3':search_member,
        '4':update_member, '5':delete_member, '6':expiring_soon,
        '7':birthdays_this_month, '8':lambda: os.system('cls' if os.name=='nt' else 'clear')
    }
    while True:
        print(f"\n{C.CY}{'='*43}{C.E}")
        print(f"{C.BO}{C.M}        GYM & DIET MANAGER{C.E}")
        print(f"{C.CY}{'='*43}{C.E}")
        opts = ["Add Member","View All","Search","Update","Delete",
                "Expiring Soon","Birthdays","Clear Screen","Exit"]
        for i,o in enumerate(opts,1): print(f"{i}. {o}")
        print(f"{C.CY}{'='*43}{C.E}")
        ch = input(f"{C.Y}Choice (1-9): {C.E}").strip()
        if ch == '9': print(f"\n{C.G} Bye!{C.E}"); break
        elif ch in menu: menu[ch]()
        else: print(f"{C.R}❌ Invalid!{C.E}")

if __name__ == '__main__':
    main()