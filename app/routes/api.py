"""
REST API routes for Thendral City Developers Website
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Project, Service, Testimonial, ImageGallery
from app.utils.decorators import api_login_required

api_bp = Blueprint('api', __name__)


# Projects API
@api_bp.route('/projects', methods=['GET'])
def get_projects():
    """
    Get all projects with optional category filter
    
    Query Params:
        category: Filter by category (current/completed)
    
    Returns:
        JSON response with projects list
    """
    category = request.args.get('category')
    
    query = db.session.query(Project).filter_by(status='active')
    
    if category in ['current', 'completed']:
        query = query.filter_by(category=category)
    
    projects = query.order_by(Project.display_order.asc()).all()
    
    return jsonify({
        'success': True,
        'data': [project.to_dict() for project in projects]
    })


@api_bp.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    """
    Get single project by ID
    
    Args:
        id: Project ID
    
    Returns:
        JSON response with project data
    """
    project = db.session.query(Project).get_or_404(id)
    
    return jsonify({
        'success': True,
        'data': project.to_dict()
    })


@api_bp.route('/projects', methods=['POST'])
@api_login_required
def create_project():
    """
    Create new project (admin only)
    
    Returns:
        JSON response with created project data
    """
    data = request.get_json()
    
    try:
        project = Project(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category', 'current'),
            client=data.get('client'),
            location=data.get('location'),
            image=data.get('image'),
            status='active',
            display_order=data.get('display_order', 0)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/projects/<int:id>', methods=['PUT'])
@api_login_required
def update_project(id):
    """
    Update existing project (admin only)
    
    Args:
        id: Project ID
    
    Returns:
        JSON response with updated project data
    """
    project = db.session.query(Project).get_or_404(id)
    data = request.get_json()
    
    try:
        if 'title' in data:
            project.title = data['title']
        if 'description' in data:
            project.description = data['description']
        if 'category' in data:
            project.category = data['category']
        if 'client' in data:
            project.client = data['client']
        if 'location' in data:
            project.location = data['location']
        if 'image' in data:
            project.image = data['image']
        if 'display_order' in data:
            project.display_order = data['display_order']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': project.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/projects/<int:id>', methods=['DELETE'])
@api_login_required
def delete_project(id):
    """
    Delete project (admin only)
    
    Args:
        id: Project ID
    
    Returns:
        JSON response
    """
    project = db.session.query(Project).get_or_404(id)
    
    try:
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Services API
@api_bp.route('/services', methods=['GET'])
def get_services():
    """
    Get all services
    
    Returns:
        JSON response with services list
    """
    services = db.session.query(Service).filter_by(status='active').order_by(Service.display_order.asc()).all()
    
    return jsonify({
        'success': True,
        'data': [service.to_dict() for service in services]
    })


@api_bp.route('/services/<int:id>', methods=['GET'])
def get_service(id):
    """
    Get single service by ID
    
    Args:
        id: Service ID
    
    Returns:
        JSON response with service data
    """
    service = db.session.query(Service).get_or_404(id)
    
    return jsonify({
        'success': True,
        'data': service.to_dict()
    })


@api_bp.route('/services', methods=['POST'])
@api_login_required
def create_service():
    """
    Create new service (admin only)
    
    Returns:
        JSON response with created service data
    """
    data = request.get_json()
    
    try:
        service = Service(
            title=data.get('title'),
            description=data.get('description'),
            icon=data.get('icon'),
            image=data.get('image'),
            status='active',
            display_order=data.get('display_order', 0)
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': service.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/services/<int:id>', methods=['PUT'])
@api_login_required
def update_service(id):
    """
    Update existing service (admin only)
    
    Args:
        id: Service ID
    
    Returns:
        JSON response with updated service data
    """
    service = db.session.query(Service).get_or_404(id)
    data = request.get_json()
    
    try:
        if 'title' in data:
            service.title = data['title']
        if 'description' in data:
            service.description = data['description']
        if 'icon' in data:
            service.icon = data['icon']
        if 'image' in data:
            service.image = data['image']
        if 'display_order' in data:
            service.display_order = data['display_order']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': service.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/services/<int:id>', methods=['DELETE'])
@api_login_required
def delete_service(id):
    """
    Delete service (admin only)
    
    Args:
        id: Service ID
    
    Returns:
        JSON response
    """
    service = db.session.query(Service).get_or_404(id)
    
    try:
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Service deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Testimonials API
@api_bp.route('/testimonials', methods=['GET'])
def get_testimonials():
    """
    Get all testimonials (featured by default)
    
    Query Params:
        featured: Filter by featured status (true/false)
    
    Returns:
        JSON response with testimonials list
    """
    featured = request.args.get('featured', 'true').lower() == 'true'
    
    query = db.session.query(Testimonial).filter_by(status='active')
    
    if featured:
        query = query.filter_by(featured=True)
    
    testimonials = query.all()
    
    return jsonify({
        'success': True,
        'data': [testimonial.to_dict() for testimonial in testimonials]
    })


# Images API
@api_bp.route('/images', methods=['POST'])
@api_login_required
def upload_image():
    """
    Upload image file (admin only)
    
    Returns:
        JSON response with image data
    """
    from app.utils.validators import validate_image_file
    from flask import current_app
    
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided'
        }), 400
    
    file = request.files['file']
    
    is_valid, error = validate_image_file(file)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': error
        }), 400
    
    try:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        image = ImageGallery(
            filename=filename,
            file_path=upload_path,
            file_size=os.path.getsize(upload_path),
            mime_type=file.content_type,
            related_to=request.form.get('related_to', 'general'),
            related_id=request.form.get('related_id'),
            uploaded_by=current_user.id
        )
        
        db.session.add(image)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': image.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/images/<int:id>', methods=['DELETE'])
@api_login_required
def delete_image(id):
    """
    Delete image (admin only)
    
    Args:
        id: Image ID
    
    Returns:
        JSON response
    """
    image = db.session.query(ImageGallery).get_or_404(id)
    
    try:
        # Delete file from disk
        if os.path.exists(image.file_path):
            os.remove(image.file_path)
        
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Image deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/images', methods=['GET'])
def get_images():
    """
    Get all images
    
    Query Params:
        related_to: Filter by related entity type
        related_id: Filter by related entity ID
    
    Returns:
        JSON response with images list
    """
    query = db.session.query(ImageGallery)
    
    related_to = request.args.get('related_to')
    related_id = request.args.get('related_id')
    
    if related_to:
        query = query.filter_by(related_to=related_to)
    
    if related_id:
        query = query.filter_by(related_id=int(related_id))
    
    images = query.order_by(ImageGallery.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [image.to_dict() for image in images]
    })
