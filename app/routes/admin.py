"""
Admin routes for Thendral City Developers Website
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Project, Service, Testimonial, ContactMessage, TeamMember, ImageGallery
from app.models.project import ProjectPhoto
from app.utils.decorators import admin_required
from app.services.auth_service import hash_password, verify_password
from werkzeug.utils import secure_filename
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Admin login page
    
    GET: Render login form
    POST: Process login credentials
    
    Returns:
        Rendered login template or redirect to dashboard
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.session.query(User).filter_by(username=username).first()
        
        if user and verify_password(password, user.password_hash):
            if user.is_admin:
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Access denied. Admin privileges required.', 'danger')
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    """
    Admin logout
    
    Returns:
        Redirect to login page
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Admin dashboard with statistics
    
    Returns:
        Rendered dashboard template with stats
    """
    stats = {
        'total_projects': db.session.query(Project).count(),
        'current_projects': db.session.query(Project).filter_by(category='current').count(),
        'completed_projects': db.session.query(Project).filter_by(category='completed').count(),
        'total_services': db.session.query(Service).count(),
        'total_testimonials': db.session.query(Testimonial).count(),
        'unread_messages': db.session.query(ContactMessage).filter_by(is_read=False).count(),
        'total_team_members': db.session.query(TeamMember).count()
    }
    
    recent_messages = db.session.query(ContactMessage).order_by(
        ContactMessage.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_messages=recent_messages)


# Project Management Routes
@admin_bp.route('/projects')
@login_required
@admin_required
def projects_list():
    """
    List all projects
    
    Returns:
        Rendered projects list template
    """
    projects = db.session.query(Project).order_by(Project.display_order.asc()).all()
    return render_template('admin/projects.html', projects=projects)


@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
@admin_required
def project_new():
    """
    Create new project
    
    GET: Render new project form
    POST: Create project
    
    Returns:
        Rendered form template or redirect to projects list
    """
    if request.method == 'POST':
        try:
            # Handle main image upload
            image_path = request.form.get('image', '')
            if 'main_image' in request.files:
                file = request.files['main_image']
                if file and file.filename:
                    from flask import current_app
                    filename = secure_filename(file.filename)
                    upload_dir = os.path.join(current_app.static_folder, 'uploads', 'projects')
                    os.makedirs(upload_dir, exist_ok=True)
                    file.save(os.path.join(upload_dir, filename))
                    image_path = f'uploads/projects/{filename}'

            project = Project(
                title=request.form.get('title'),
                short_description=request.form.get('short_description'),
                description=request.form.get('description'),
                category=request.form.get('category'),
                client=request.form.get('client'),
                location=request.form.get('location'),
                area_sqft=request.form.get('area_sqft'),
                floors=request.form.get('floors'),
                project_type=request.form.get('project_type'),
                start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d') if request.form.get('start_date') else None,
                completion_date=datetime.strptime(request.form.get('completion_date'), '%Y-%m-%d') if request.form.get('completion_date') else None,
                image=image_path,
                youtube_url=request.form.get('youtube_url'),
                status='active',
                display_order=int(request.form.get('display_order', 0))
            )
            
            db.session.add(project)
            db.session.flush()  # get ID for photo uploads
            
            # Handle multiple photo uploads (up to 6)
            from flask import current_app
            upload_dir = os.path.join(current_app.static_folder, 'uploads', 'projects')
            os.makedirs(upload_dir, exist_ok=True)
            
            for i in range(1, 7):
                photo_file = request.files.get(f'photo_{i}')
                if photo_file and photo_file.filename:
                    fname = secure_filename(photo_file.filename)
                    photo_file.save(os.path.join(upload_dir, fname))
                    caption = request.form.get(f'photo_caption_{i}', '')
                    photo = ProjectPhoto(
                        project_id=project.id,
                        filename=fname,
                        file_path=f'uploads/projects/{fname}',
                        caption=caption,
                        display_order=i
                    )
                    db.session.add(photo)
            
            db.session.commit()
            flash('Project created successfully!', 'success')
            return redirect(url_for('admin.projects_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating project: {str(e)}', 'danger')
    
    return render_template('admin/project_form.html', project=None, photos=[])


@admin_bp.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def project_edit(id):
    """
    Edit existing project
    
    Args:
        id: Project ID
    
    Returns:
        Rendered edit form template or redirect to projects list
    """
    project = db.session.query(Project).get_or_404(id)
    existing_photos = db.session.query(ProjectPhoto).filter_by(project_id=id).order_by(ProjectPhoto.display_order).all()
    
    if request.method == 'POST':
        try:
            from flask import current_app
            project.title = request.form.get('title')
            project.short_description = request.form.get('short_description')
            project.description = request.form.get('description')
            project.category = request.form.get('category')
            project.client = request.form.get('client')
            project.location = request.form.get('location')
            project.area_sqft = request.form.get('area_sqft')
            project.floors = request.form.get('floors')
            project.project_type = request.form.get('project_type')
            project.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d') if request.form.get('start_date') else None
            project.completion_date = datetime.strptime(request.form.get('completion_date'), '%Y-%m-%d') if request.form.get('completion_date') else None
            project.youtube_url = request.form.get('youtube_url')
            project.display_order = int(request.form.get('display_order', 0))
            
            # Main image upload
            if 'main_image' in request.files:
                file = request.files['main_image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    upload_dir = os.path.join(current_app.static_folder, 'uploads', 'projects')
                    os.makedirs(upload_dir, exist_ok=True)
                    file.save(os.path.join(upload_dir, filename))
                    project.image = f'uploads/projects/{filename}'
            elif request.form.get('image'):
                project.image = request.form.get('image')
            
            # Additional photo uploads
            upload_dir = os.path.join(current_app.static_folder, 'uploads', 'projects')
            os.makedirs(upload_dir, exist_ok=True)
            current_count = db.session.query(ProjectPhoto).filter_by(project_id=id).count()
            
            for i in range(1, 7):
                photo_file = request.files.get(f'photo_{i}')
                if photo_file and photo_file.filename and current_count < 6:
                    fname = secure_filename(photo_file.filename)
                    photo_file.save(os.path.join(upload_dir, fname))
                    caption = request.form.get(f'photo_caption_{i}', '')
                    photo = ProjectPhoto(
                        project_id=project.id,
                        filename=fname,
                        file_path=f'uploads/projects/{fname}',
                        caption=caption,
                        display_order=current_count + i
                    )
                    db.session.add(photo)
                    current_count += 1
            
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin.projects_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {str(e)}', 'danger')
    
    return render_template('admin/project_form.html', project=project, photos=existing_photos)


@admin_bp.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def project_delete(id):
    """
    Delete project
    
    Args:
        id: Project ID
    
    Returns:
        JSON response or redirect
    """
    project = db.session.query(Project).get_or_404(id)
    
    try:
        db.session.delete(project)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True})
        
        flash('Project deleted successfully!', 'success')
        return redirect(url_for('admin.projects_list'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        
        flash(f'Error deleting project: {str(e)}', 'danger')
        return redirect(url_for('admin.projects_list'))


@admin_bp.route('/projects/<int:project_id>/photos/<int:photo_id>/delete', methods=['POST'])
@login_required
@admin_required
def project_photo_delete(project_id, photo_id):
    """Delete a single project photo"""
    photo = db.session.query(ProjectPhoto).filter_by(id=photo_id, project_id=project_id).first_or_404()
    try:
        db.session.delete(photo)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# Service Management Routes
@admin_bp.route('/services')
@login_required
@admin_required
def services_list():
    """
    List all services
    
    Returns:
        Rendered services list template
    """
    services = db.session.query(Service).order_by(Service.display_order.asc()).all()
    return render_template('admin/services.html', services=services)


@admin_bp.route('/services/new', methods=['GET', 'POST'])
@login_required
@admin_required
def service_new():
    """
    Create new service
    
    Returns:
        Rendered form template or redirect to services list
    """
    if request.method == 'POST':
        try:
            service = Service(
                title=request.form.get('title'),
                description=request.form.get('description'),
                icon=request.form.get('icon'),
                image=request.form.get('image'),
                status='active',
                display_order=int(request.form.get('display_order', 0))
            )
            
            db.session.add(service)
            db.session.commit()
            
            flash('Service created successfully!', 'success')
            return redirect(url_for('admin.services_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating service: {str(e)}', 'danger')
    
    return render_template('admin/service_form.html', service=None)


@admin_bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def service_edit(id):
    """
    Edit existing service
    
    Args:
        id: Service ID
    
    Returns:
        Rendered edit form template or redirect to services list
    """
    service = db.session.query(Service).get_or_404(id)
    
    if request.method == 'POST':
        try:
            service.title = request.form.get('title')
            service.description = request.form.get('description')
            service.icon = request.form.get('icon')
            service.image = request.form.get('image')
            service.display_order = int(request.form.get('display_order', 0))
            
            db.session.commit()
            
            flash('Service updated successfully!', 'success')
            return redirect(url_for('admin.services_list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating service: {str(e)}', 'danger')
    
    return render_template('admin/service_form.html', service=service)


@admin_bp.route('/services/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def service_delete(id):
    """
    Delete service
    
    Args:
        id: Service ID
    
    Returns:
        JSON response or redirect
    """
    service = db.session.query(Service).get_or_404(id)
    
    try:
        db.session.delete(service)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True})
        
        flash('Service deleted successfully!', 'success')
        return redirect(url_for('admin.services_list'))
        
    except Exception as e:
        db.session.rollback()
        
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        
        flash(f'Error deleting service: {str(e)}', 'danger')
        return redirect(url_for('admin.services_list'))


# Contact Messages Routes
@admin_bp.route('/messages')
@login_required
@admin_required
def messages_list():
    """
    List all contact messages
    
    Returns:
        Rendered messages list template
    """
    messages = db.session.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)


@admin_bp.route('/messages/<int:id>/mark-read', methods=['POST'])
@login_required
@admin_required
def message_mark_read(id):
    """
    Mark message as read
    
    Args:
        id: Message ID
    
    Returns:
        JSON response
    """
    message = db.session.query(ContactMessage).get_or_404(id)
    message.is_read = True
    db.session.commit()
    
    return jsonify({'success': True})


@admin_bp.route('/messages/<int:id>/mark-responded', methods=['POST'])
@login_required
@admin_required
def message_mark_responded(id):
    """
    Mark message as responded
    
    Args:
        id: Message ID
    
    Returns:
        JSON response
    """
    message = db.session.query(ContactMessage).get_or_404(id)
    message.is_responded = True
    db.session.commit()
    
    return jsonify({'success': True})
