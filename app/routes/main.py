"""
Main public routes for Thendral City Developers Website
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app import db
from app.models import Project, Service, Testimonial, ContactMessage
from datetime import datetime

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Home page route - using hardcoded content for now
    """
    # Note: Template currently uses hardcoded project data, not database
    # Can be updated to use dynamic data when template is ready
    return render_template('index.html')


@main_bp.route('/promotings')
def promotings():
    """
    Promotings page route
    
    Returns:
        Rendered promotings.html template
    """
    return render_template('promotings.html')


@main_bp.route('/quality')
def quality():
    """
    Quality page route
    
    Returns:
        Rendered quality.html template
    """
    return render_template('quality.html')


@main_bp.route('/nri')
def nri():
    """
    NRI page route
    
    Returns:
        Rendered nri.html template
    """
    return render_template('nri.html')


@main_bp.route('/residential')
def residential():
    """
    Residential page route
    
    Returns:
        Rendered residential.html template
    """
    return render_template('residential.html')


@main_bp.route('/careers')
def careers():
    """
    Careers page route
    
    Returns:
        Rendered careers.html template
    """
    return render_template('careers.html')


@main_bp.route('/services')
def services():
    """
    Services page route
    
    Returns:
        Rendered services.html template
    """
    return render_template('services.html')


@main_bp.route('/projects')
def projects():
    """
    Projects page route
    
    Args:
        category: Optional category filter (current/completed)
    
    Returns:
        Rendered projects.html template with filtered projects
    """
    category = request.args.get('category')
    
    if category in ['current', 'completed']:
        projects_list = db.session.query(Project).filter_by(
            category=category,
            status='active'
        ).order_by(Project.display_order.asc()).all()
    else:
        projects_list = db.session.query(Project).filter_by(
            status='active'
        ).order_by(Project.display_order.asc()).all()
    
    return render_template('projects.html', projects=projects_list, active_tab=category or 'all')


@main_bp.route('/projects/<int:project_id>')
def project_detail(project_id):
    """
    Single project detail page with gallery and YouTube embed
    """
    from app.models.project import ProjectPhoto
    project = db.session.query(Project).filter_by(id=project_id, status='active').first_or_404()
    photos = db.session.query(ProjectPhoto).filter_by(project_id=project_id).order_by(ProjectPhoto.display_order).all()
    related = db.session.query(Project).filter(
        Project.category == project.category,
        Project.status == 'active',
        Project.id != project_id
    ).limit(3).all()
    return render_template('project_detail.html', project=project, photos=photos, related=related)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Contact page route
    """
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
                
            from app.utils.validators import sanitize_string
            
            # Create new contact message with sanitized input
            message = ContactMessage(
                name=sanitize_string(data.get('name'), 100),
                email=sanitize_string(data.get('email'), 100),
                phone=sanitize_string(data.get('phone'), 20),
                subject=sanitize_string(data.get('subject'), 200),
                message=sanitize_string(data.get('message'), 2000),
                is_read=False,
                is_responded=False
            )
            
            db.session.add(message)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            # Log the error but don't leak details to the client
            print(f"Contact form error: {e}") 
            return jsonify({'success': False, 'error': 'An internal error occurred. Please try again later.'}), 500
    
    return render_template('contact.html')


@main_bp.route('/robots.txt')
def robots():
    """
    Serve robots.txt for SEO and security
    """
    content = "User-agent: *\nDisallow: /admin/\nDisallow: /api/\nSitemap: " + request.url_root + "sitemap.xml"
    return content, 200, {'Content-Type': 'text/plain'}


@main_bp.route('/sitemap.xml')
def sitemap():
    """
    Generate dynamic sitemap for Google indexing
    """
    pages = []
    # Static pages
    for rule in [
        'main.index', 'main.projects', 'main.services', 'main.promotings', 
        'main.quality', 'main.nri', 'main.residential', 'main.careers', 'main.contact'
    ]:
        pages.append({
            'loc': url_for(rule, _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })
    
    # Dynamic projects
    projects_list = db.session.query(Project).filter_by(status='active').all()
    for p in projects_list:
        pages.append({
            'loc': url_for('main.project_detail', project_id=p.id, _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })
        
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    return sitemap_xml, 200, {'Content-Type': 'application/xml'}




@main_bp.route('/api/projects')
def api_projects():
    """
    API endpoint to get projects
    
    Args:
        category: Optional category filter (current/completed)
    
    Returns:
        JSON response with projects data
    """
    category = request.args.get('category')
    
    if category in ['current', 'completed']:
        projects_list = db.session.query(Project).filter_by(
            category=category,
            status='active'
        ).order_by(Project.display_order.asc()).all()
    else:
        projects_list = db.session.query(Project).filter_by(
            status='active'
        ).order_by(Project.display_order.asc()).all()
    
    return jsonify({
        'success': True,
        'projects': [project.to_dict() for project in projects_list]
    })


@main_bp.route('/api/services')
def api_services():
    """
    API endpoint to get services
    
    Returns:
        JSON response with services data
    """
    services_list = db.session.query(Service).filter_by(
        status='active'
    ).order_by(Service.display_order.asc()).all()
    
    return jsonify({
        'success': True,
        'services': [service.to_dict() for service in services_list]
    })


@main_bp.route('/api/testimonials')
def api_testimonials():
    """
    API endpoint to get testimonials
    
    Returns:
        JSON response with testimonials data
    """
    testimonials_list = db.session.query(Testimonial).filter_by(
        status='active',
        featured=True
    ).all()
    
    return jsonify({
        'success': True,
        'testimonials': [testimonial.to_dict() for testimonial in testimonials_list]
    })
