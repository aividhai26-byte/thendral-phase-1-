"""
Project Service - Business logic for project operations
"""

from app.models import Project
from app import db
from datetime import datetime


class ProjectService:
    """Service class for project operations"""
    
    @staticmethod
    def get_projects(category=None, status='active'):
        """
        Get projects with optional filters
        
        Args:
            category: Filter by category (current/completed)
            status: Filter by status (default: active)
        
        Returns:
            Query object for projects
        """
        query = Project.query
        
        if category:
            query = query.filter_by(category=category)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(Project.display_order.asc())
    
    @staticmethod
    def get_project(project_id):
        """
        Get single project by ID
        
        Args:
            project_id: ID of the project
        
        Returns:
            Project object or None
        """
        return Project.query.get(project_id)
    
    @staticmethod
    def create_project(data, image=None):
        """
        Create new project
        
        Args:
            data: Dictionary with project data
            image: Optional image path
        
        Returns:
            Created Project object or None if failed
        """
        try:
            project = Project(
                title=data.get('title'),
                description=data.get('description'),
                category=data.get('category', 'current'),
                client=data.get('client'),
                location=data.get('location'),
                start_date=datetime.strptime(data['start_date'], '%Y-%m-%d') if data.get('start_date') else None,
                completion_date=datetime.strptime(data['completion_date'], '%Y-%m-%d') if data.get('completion_date') else None,
                image=image or data.get('image'),
                status='active',
                display_order=data.get('display_order', 0)
            )
            
            db.session.add(project)
            db.session.commit()
            
            return project
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating project: {e}")
            return None
    
    @staticmethod
    def update_project(project_id, data, image=None):
        """
        Update existing project
        
        Args:
            project_id: ID of the project to update
            data: Dictionary with updated project data
            image: Optional new image path
        
        Returns:
            Updated Project object or None if failed
        """
        try:
            project = Project.query.get(project_id)
            
            if not project:
                return None
            
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
            if 'start_date' in data and data['start_date']:
                project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            if 'completion_date' in data and data['completion_date']:
                project.completion_date = datetime.strptime(data['completion_date'], '%Y-%m-%d')
            if image:
                project.image = image
            elif 'image' in data:
                project.image = data['image']
            if 'display_order' in data:
                project.display_order = data['display_order']
            if 'status' in data:
                project.status = data['status']
            
            db.session.commit()
            
            return project
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating project: {e}")
            return None
    
    @staticmethod
    def delete_project(project_id):
        """
        Delete project
        
        Args:
            project_id: ID of the project to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            project = Project.query.get(project_id)
            
            if not project:
                return False
            
            db.session.delete(project)
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting project: {e}")
            return False
    
    @staticmethod
    def update_display_order(project_orders):
        """
        Update display order for multiple projects
        
        Args:
            project_orders: Dictionary mapping project IDs to display orders
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            for project_id, order in project_orders.items():
                project = Project.query.get(project_id)
                if project:
                    project.display_order = order
            
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating display order: {e}")
            return False
