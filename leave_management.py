import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib

# Initialize session state data
def init_data():
    """Initialize demo data in session state"""
    if 'employees' not in st.session_state:
        st.session_state.employees = {
            1001: {'emp_id': 1001, 'name': 'John Doe', 'email': 'john.doe@acme.com', 
                   'password': hashlib.sha256('password123'.encode()).hexdigest(), 
                   'department': 'Engineering', 'role': 'Employee', 'total_leaves': 20, 'used_leaves': 5},
            1002: {'emp_id': 1002, 'name': 'Jane Smith', 'email': 'jane.smith@acme.com', 
                   'password': hashlib.sha256('password123'.encode()).hexdigest(), 
                   'department': 'Engineering', 'role': 'Manager', 'total_leaves': 20, 'used_leaves': 3},
            1003: {'emp_id': 1003, 'name': 'Bob Johnson', 'email': 'bob.johnson@acme.com', 
                   'password': hashlib.sha256('password123'.encode()).hexdigest(), 
                   'department': 'HR', 'role': 'Employee', 'total_leaves': 20, 'used_leaves': 8},
            1004: {'emp_id': 1004, 'name': 'Alice Williams', 'email': 'alice.williams@acme.com', 
                   'password': hashlib.sha256('password123'.encode()).hexdigest(), 
                   'department': 'Marketing', 'role': 'Employee', 'total_leaves': 20, 'used_leaves': 2},
            1005: {'emp_id': 1005, 'name': 'Charlie Brown', 'email': 'charlie.brown@acme.com', 
                   'password': hashlib.sha256('password123'.encode()).hexdigest(), 
                   'department': 'Sales', 'role': 'Manager', 'total_leaves': 20, 'used_leaves': 4},
            1006: {'emp_id': 1006, 'name': 'Diana Prince', 'email': 'diana.prince@acme.com', 
                   'password': hashlib.sha256('password123'.encode()).hexdigest(), 
                   'department': 'Engineering', 'role': 'Employee', 'total_leaves': 20, 'used_leaves': 6},
            1007: {'emp_id': 1007, 'name': 'Eve Davis', 'email': 'eve.davis@acme.com', 
                   'password': hashlib.sha256('password123'.encode()).hexdigest(), 
                   'department': 'HR', 'role': 'Manager', 'total_leaves': 20, 'used_leaves': 1},
        }
    
    if 'leave_requests' not in st.session_state:
        st.session_state.leave_requests = [
            {'request_id': 1, 'emp_id': 1001, 'leave_type': 'Sick Leave', 'start_date': '2025-11-15', 
             'end_date': '2025-11-17', 'days': 3, 'reason': 'Medical appointment', 
             'status': 'Approved', 'applied_date': '2025-11-10 09:30:00', 'approved_by': 1002},
            {'request_id': 2, 'emp_id': 1001, 'leave_type': 'Casual Leave', 'start_date': '2025-12-20', 
             'end_date': '2025-12-22', 'days': 2, 'reason': 'Personal work', 
             'status': 'Pending', 'applied_date': '2025-12-15 14:20:00', 'approved_by': None},
            {'request_id': 3, 'emp_id': 1003, 'leave_type': 'Annual Leave', 'start_date': '2025-11-01', 
             'end_date': '2025-11-08', 'days': 8, 'reason': 'Vacation', 
             'status': 'Approved', 'applied_date': '2025-10-25 11:00:00', 'approved_by': 1007},
            {'request_id': 4, 'emp_id': 1004, 'leave_type': 'Casual Leave', 'start_date': '2025-11-25', 
             'end_date': '2025-11-26', 'days': 2, 'reason': 'Family function', 
             'status': 'Approved', 'applied_date': '2025-11-20 16:45:00', 'approved_by': 1002},
            {'request_id': 5, 'emp_id': 1006, 'leave_type': 'Sick Leave', 'start_date': '2025-12-01', 
             'end_date': '2025-12-03', 'days': 3, 'reason': 'Flu', 
             'status': 'Rejected', 'applied_date': '2025-11-28 08:15:00', 'approved_by': 1002},
            {'request_id': 6, 'emp_id': 1006, 'leave_type': 'Casual Leave', 'start_date': '2025-12-15', 
             'end_date': '2025-12-17', 'days': 3, 'reason': 'Personal work', 
             'status': 'Pending', 'applied_date': '2025-12-10 10:30:00', 'approved_by': None},
        ]
        st.session_state.next_request_id = 7

# Authentication functions
def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Authenticate user credentials"""
    hashed_password = hash_password(password)
    for emp_id, emp in st.session_state.employees.items():
        if emp['email'] == email and emp['password'] == hashed_password:
            return emp.copy()
    return None

# Leave management functions
def apply_leave(emp_id, leave_type, start_date, end_date, reason):
    """Apply for a new leave"""
    days = (end_date - start_date).days + 1
    
    new_request = {
        'request_id': st.session_state.next_request_id,
        'emp_id': emp_id,
        'leave_type': leave_type,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'days': days,
        'reason': reason,
        'status': 'Pending',
        'applied_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'approved_by': None
    }
    
    st.session_state.leave_requests.append(new_request)
    st.session_state.next_request_id += 1
    return True

def get_employee_leaves(emp_id):
    """Get all leave requests for an employee"""
    leaves = [req for req in st.session_state.leave_requests if req['emp_id'] == emp_id]
    return pd.DataFrame(leaves) if leaves else pd.DataFrame()

def get_all_leave_requests():
    """Get all leave requests (for managers)"""
    data = []
    for req in st.session_state.leave_requests:
        emp = st.session_state.employees[req['emp_id']]
        data.append({
            'request_id': req['request_id'],
            'name': emp['name'],
            'department': emp['department'],
            'leave_type': req['leave_type'],
            'start_date': req['start_date'],
            'end_date': req['end_date'],
            'days': req['days'],
            'reason': req['reason'],
            'status': req['status'],
            'applied_date': req['applied_date']
        })
    return pd.DataFrame(data) if data else pd.DataFrame()

def update_leave_status(request_id, status, manager_id):
    """Update leave request status"""
    for req in st.session_state.leave_requests:
        if req['request_id'] == request_id:
            req['status'] = status
            req['approved_by'] = manager_id
            
            # If approved, update employee's used leaves
            if status == 'Approved':
                emp_id = req['emp_id']
                st.session_state.employees[emp_id]['used_leaves'] += req['days']
            break

def get_leave_statistics(emp_id):
    """Get leave statistics for an employee"""
    emp = st.session_state.employees[emp_id]
    return {
        'total': emp['total_leaves'],
        'used': emp['used_leaves'],
        'available': emp['total_leaves'] - emp['used_leaves']
    }

# Streamlit UI
def main():
    st.set_page_config(
        page_title="ACME Leave Management System",
        page_icon="🏢",
        layout="wide"
    )
    
    # Initialize data
    init_data()
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Session state initialization
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
    
    # Login page
    if not st.session_state.logged_in:
        st.markdown('<div class="main-header">🏢 ACME Leave Management System</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Login")
            
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="your.email@acme.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    if email and password:
                        user = authenticate_user(email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")
                    else:
                        st.error("❌ Please enter both email and password.")
            
            st.info("💡 **Demo Credentials:**\n\n**Employee:** john.doe@acme.com / password123\n\n**Manager:** jane.smith@acme.com / password123")
    
    # Main application
    else:
        user = st.session_state.user
        
        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<div class="main-header">🏢 ACME Leave Management System</div>', unsafe_allow_html=True)
        with col2:
            st.write(f"**Welcome, {user['name']}**")
            st.write(f"*{user['role']} - {user['department']}*")
            if st.button("Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.rerun()
        
        st.divider()
        
        # Navigation tabs
        if user['role'] == 'Manager':
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "➕ Apply Leave", "📋 My Leaves", "✅ Approve Leaves"])
        else:
            tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Apply Leave", "📋 My Leaves"])
        
        # Dashboard Tab
        with tab1:
            st.header("📊 Leave Dashboard")
            
            stats = get_leave_statistics(user['emp_id'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <div class="stat-value">{stats['total']}</div>
                        <div class="stat-label">Total Leaves</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <div class="stat-value">{stats['used']}</div>
                        <div class="stat-label">Used Leaves</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                        <div class="stat-value">{stats['available']}</div>
                        <div class="stat-label">Available Leaves</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Recent leave requests
            st.subheader("📅 Recent Leave Requests")
            leaves_df = get_employee_leaves(user['emp_id'])
            
            if not leaves_df.empty:
                display_df = leaves_df.copy()
                display_df = display_df.sort_values('applied_date', ascending=False)
                
                st.dataframe(
                    display_df[['request_id', 'leave_type', 'start_date', 'end_date', 'days', 'reason', 'status']],
                    column_config={
                        "request_id": "Request ID",
                        "leave_type": "Leave Type",
                        "start_date": "Start Date",
                        "end_date": "End Date",
                        "days": "Days",
                        "reason": "Reason",
                        "status": "Status"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No leave requests found.")
        
        # Apply Leave Tab
        with tab2:
            st.header("➕ Apply for Leave")
            
            col1, col2 = st.columns(2)
            
            with col1:
                leave_type = st.selectbox(
                    "Leave Type",
                    ["Casual Leave", "Sick Leave", "Annual Leave", "Maternity Leave", "Paternity Leave"]
                )
                start_date = st.date_input("Start Date", min_value=datetime.now().date())
            
            with col2:
                end_date = st.date_input("End Date", min_value=datetime.now().date())
                
            reason = st.text_area("Reason for Leave", placeholder="Please provide a reason for your leave request...")
            
            if st.button("Submit Leave Request", type="primary", use_container_width=True):
                if start_date > end_date:
                    st.error("❌ End date must be after start date!")
                elif not reason.strip():
                    st.error("❌ Please provide a reason for your leave request!")
                else:
                    days_requested = (end_date - start_date).days + 1
                    stats = get_leave_statistics(user['emp_id'])
                    
                    if days_requested > stats['available']:
                        st.error(f"❌ Insufficient leave balance! You have only {stats['available']} days available.")
                    else:
                        apply_leave(user['emp_id'], leave_type, start_date, end_date, reason)
                        st.success(f"✅ Leave request submitted successfully for {days_requested} days!")
                        st.balloons()
        
        # My Leaves Tab
        with tab3:
            st.header("📋 My Leave History")
            
            leaves_df = get_employee_leaves(user['emp_id'])
            
            if not leaves_df.empty:
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    status_filter = st.multiselect(
                        "Filter by Status",
                        options=['Pending', 'Approved', 'Rejected'],
                        default=['Pending', 'Approved', 'Rejected']
                    )
                
                with col2:
                    leave_type_filter = st.multiselect(
                        "Filter by Leave Type",
                        options=leaves_df['leave_type'].unique(),
                        default=leaves_df['leave_type'].unique()
                    )
                
                # Apply filters
                filtered_df = leaves_df[
                    (leaves_df['status'].isin(status_filter)) &
                    (leaves_df['leave_type'].isin(leave_type_filter))
                ]
                
                filtered_df = filtered_df.sort_values('applied_date', ascending=False)
                
                st.dataframe(
                    filtered_df[['request_id', 'leave_type', 'start_date', 'end_date', 'days', 'reason', 'status', 'applied_date']],
                    column_config={
                        "request_id": "Request ID",
                        "leave_type": "Leave Type",
                        "start_date": "Start Date",
                        "end_date": "End Date",
                        "days": "Days",
                        "reason": "Reason",
                        "status": "Status",
                        "applied_date": "Applied On"
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                st.info(f"📊 Showing {len(filtered_df)} of {len(leaves_df)} leave requests")
            else:
                st.info("No leave requests found.")
        
        # Approve Leaves Tab (Manager only)
        if user['role'] == 'Manager':
            with tab4:
                st.header("✅ Approve Leave Requests")
                
                all_leaves_df = get_all_leave_requests()
                
                if not all_leaves_df.empty:
                    # Filter for pending requests
                    pending_df = all_leaves_df[all_leaves_df['status'] == 'Pending']
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.subheader(f"Pending Requests ({len(pending_df)})")
                    with col2:
                        show_all = st.checkbox("Show All Requests")
                    
                    display_df = all_leaves_df if show_all else pending_df
                    
                    if not display_df.empty:
                        for idx, row in display_df.iterrows():
                            with st.container():
                                col1, col2, col3, col4 = st.columns([2, 2, 3, 2])
                                
                                with col1:
                                    st.write(f"**{row['name']}**")
                                    st.caption(f"{row['department']}")
                                
                                with col2:
                                    st.write(f"**{row['leave_type']}**")
                                    st.caption(f"{row['days']} days")
                                
                                with col3:
                                    st.write(f"{row['start_date']} to {row['end_date']}")
                                    st.caption(f"Reason: {row['reason']}")
                                
                                with col4:
                                    if row['status'] == 'Pending':
                                        col_a, col_b = st.columns(2)
                                        with col_a:
                                            if st.button("✅", key=f"approve_{row['request_id']}", use_container_width=True):
                                                update_leave_status(row['request_id'], 'Approved', user['emp_id'])
                                                st.success("Approved!")
                                                st.rerun()
                                        with col_b:
                                            if st.button("❌", key=f"reject_{row['request_id']}", use_container_width=True):
                                                update_leave_status(row['request_id'], 'Rejected', user['emp_id'])
                                                st.error("Rejected!")
                                                st.rerun()
                                    else:
                                        status_color = "green" if row['status'] == 'Approved' else "red"
                                        st.markdown(f":{status_color}[{row['status']}]")
                                
                                st.divider()
                    else:
                        st.info("No pending leave requests.")
                else:
                    st.info("No leave requests found.")

if __name__ == "__main__":
    main()
