"""
Database Initialization Script
Creates database tables and inserts seed data for development
"""

from app import create_app, db
from app.services.auth_service import hash_password
from datetime import datetime


def init_database():
    """
    Initialize database with seed data
    """
    app = create_app('development')
    
    with app.app_context():
        # Import models within app context
        from app.models import User, Project, ProjectPhoto, Service, Testimonial, ContactMessage, TeamMember, ImageGallery
        from app.models import Base
        
        # Create all tables using Base metadata
        Base.metadata.create_all(bind=db.engine)
        
        print("Database tables created successfully.")
        
        # Check if admin user already exists
        admin = db.session.query(User).filter_by(username='admin').first()
        
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@thendralcity.com',
                password_hash=hash_password('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            print("Admin user created (username: admin, password: admin123)")
        else:
            print("Admin user already exists.")
        
        # Check if sample projects exist
        if db.session.query(Project).count() == 0:
            # Create sample projects using local images
            projects = [
                Project(
                    title='City Center Complex',
                    short_description='Modern commercial complex with premium office spaces and retail outlets in the heart of the city.',
                    description='A landmark commercial development featuring state-of-the-art office spaces, retail outlets, and ample parking facilities. Built with precision engineering and premium materials, this complex sets the standard for modern commercial construction in Tamil Nadu.',
                    category='current',
                    client='City Developers Ltd',
                    location='Tiruppur, Tamil Nadu',
                    area_sqft='45,000 sq.ft',
                    floors='G+8',
                    project_type='Commercial Complex',
                    start_date=datetime(2024, 1, 15),
                    completion_date=datetime(2025, 12, 31),
                    image='images/7243a6b06f78c4fcae7eea862cca65e5.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=1
                ),
                Project(
                    title='Green Valley Apartments',
                    short_description='Eco-friendly residential apartments with lush green spaces and world-class modern amenities.',
                    description='Green Valley Apartments is a premium residential project featuring 120 thoughtfully designed apartments across 3 towers. Each unit is crafted with eco-friendly materials, energy-efficient systems, and surrounded by 40% green landscape.',
                    category='current',
                    client='Green Homes Pvt Ltd',
                    location='Tiruppur, Tamil Nadu',
                    area_sqft='1,80,000 sq.ft',
                    floors='G+12',
                    project_type='Residential Apartments',
                    start_date=datetime(2024, 3, 1),
                    completion_date=datetime(2025, 6, 30),
                    image='images/480251f2e693416b4dc99b5b3ea6e699.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=2
                ),
                Project(
                    title='Industrial Warehouse',
                    short_description='State-of-the-art warehouse and logistics facility built for efficiency and scalability.',
                    description='A modern industrial warehouse facility spanning over 80,000 sq.ft with advanced logistics infrastructure, automated storage systems, and easy truck access. Designed for durability and operational efficiency.',
                    category='current',
                    client='Logistics Corp India',
                    location='SIPCOT, Tamil Nadu',
                    area_sqft='80,000 sq.ft',
                    floors='Single Storey',
                    project_type='Industrial Warehouse',
                    start_date=datetime(2024, 5, 1),
                    completion_date=datetime(2025, 2, 28),
                    image='images/e8be1c833e1db3d91049cfe8fde9e3d8.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=3
                ),
                Project(
                    title='Luxury Residential Township',
                    short_description='A premium gated township with luxury villas, club house, and landscaped gardens.',
                    description='Our most prestigious completed project — a self-contained luxury township featuring 48 independent villas, a premium clubhouse, swimming pool, children\'s play area, and 5 acres of beautifully landscaped gardens. Delivered on time, exceeding client expectations.',
                    category='completed',
                    client='Premium Estates',
                    location='Tiruppur, Tamil Nadu',
                    area_sqft='2,40,000 sq.ft',
                    floors='G+2 Villas',
                    project_type='Residential Township',
                    start_date=datetime(2022, 6, 1),
                    completion_date=datetime(2023, 12, 31),
                    image='images/costructed completed buildign.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=4
                ),
                Project(
                    title='Modern Living Residences',
                    short_description='Contemporary apartment complex with smart home features and premium amenities.',
                    description='Modern Living Residences is a completed 200-unit apartment complex with smart home automation, rooftop garden, gymnasium, and dedicated parking. Recognized as the best residential project of 2023 in Tamil Nadu.',
                    category='completed',
                    client='Urban Living Developers',
                    location='Coimbatore, Tamil Nadu',
                    area_sqft='3,20,000 sq.ft',
                    floors='G+15',
                    project_type='Residential Apartments',
                    start_date=datetime(2021, 8, 1),
                    completion_date=datetime(2023, 6, 30),
                    image='images/Luxury apartment exterior — clean modern building, blue skyLandscape.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=5
                ),
                Project(
                    title='Premium Apartments Phase 2',
                    short_description='Second phase of our award-winning premium apartments with upgraded specifications.',
                    description='The highly anticipated Phase 2 expansion of our premium apartment project. Building on the success of Phase 1, this phase delivers 150 units with upgraded finishes, wider corridors, and a dedicated co-working space for residents.',
                    category='completed',
                    client='Urban Living Developers',
                    location='Coimbatore, Tamil Nadu',
                    area_sqft='2,40,000 sq.ft',
                    floors='G+12',
                    project_type='Residential Apartments',
                    start_date=datetime(2023, 1, 1),
                    completion_date=datetime(2024, 6, 30),
                    image='images/Luxury apartment exterior — clean modern building, blue skyLandscape2.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=6
                ),
            ]
            
            for project in projects:
                db.session.add(project)
            db.session.flush()  # get IDs
            
            # Add gallery photos to the first project using local images
            if projects:
                gallery_images = [
                    '7243a6b06f78c4fcae7eea862cca65e5.jpg',
                    '480251f2e693416b4dc99b5b3ea6e699.jpg',
                    'e8be1c833e1db3d91049cfe8fde9e3d8.jpg',
                    'costructed completed buildign.jpg',
                    'home1.jpg',
                    'workersonsite.jpg',
                ]
                for i, fname in enumerate(gallery_images):
                    photo = ProjectPhoto(
                        project_id=projects[0].id,
                        filename=fname,
                        file_path=f'images/{fname}',
                        caption=f'Project view {i+1}',
                        display_order=i+1
                    )
                    db.session.add(photo)
            
            print("Sample projects created.")
        else:
            print("Projects already exist.")
        
        # Check if sample services exist
        if db.session.query(Service).count() == 0:
            services = [
                Service(
                    title='Building Construction',
                    description='Complete building construction services from foundation to finishing.',
                    icon='building',
                    image='https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=600&q=80',
                    status='active',
                    display_order=1
                ),
                Service(
                    title='Interior Design',
                    description='Transform your spaces with our professional interior design services.',
                    icon='palette',
                    image='https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=600&q=80',
                    status='active',
                    display_order=2
                ),
                Service(
                    title='Renovation & Remodeling',
                    description='Breathe new life into your existing property with our renovation services.',
                    icon='tools',
                    image='https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=600&q=80',
                    status='active',
                    display_order=3
                ),
                Service(
                    title='Civil Engineering',
                    description='Expert civil engineering services including structural design and site planning.',
                    icon='drafting-compass',
                    image='https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=600&q=80',
                    status='active',
                    display_order=4
                ),
                Service(
                    title='Industrial Construction',
                    description='Specialized construction for industrial facilities and manufacturing plants.',
                    icon='factory',
                    image='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
                    status='active',
                    display_order=5
                ),
                Service(
                    title='Project Management',
                    description='End-to-end project management ensuring timely and quality delivery.',
                    icon='clipboard-list',
                    image='https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&q=80',
                    status='active',
                    display_order=6
                )
            ]
            
            for service in services:
                db.session.add(service)
            
            print("Sample services created.")
        else:
            print("Services already exist.")
        
        # Check if sample testimonials exist
        if db.session.query(Testimonial).count() == 0:
            testimonials = [
                Testimonial(
                    client_name='Ramesh Kumar',
                    company='Kumar Enterprises',
                    quote='Thendral City Developers delivered our office complex on time and within budget. Their professionalism and attention to detail are unmatched.',
                    rating=5,
                    featured=True,
                    status='active'
                ),
                Testimonial(
                    client_name='Sneha Patel',
                    company='Patel Realty',
                    quote='We hired them for our residential project and couldn\'t be happier. The quality of work exceeded our expectations.',
                    rating=5,
                    featured=True,
                    status='active'
                )
            ]
            
            for testimonial in testimonials:
                db.session.add(testimonial)
            
            print("Sample testimonials created.")
        else:
            print("Testimonials already exist.")
        
        # Commit all changes
        db.session.commit()
        
        print("\nDatabase initialization completed successfully!")
        print("\nDefault Admin Credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nPlease change the admin password after first login.")


def reset_database():
    """
    Reset database by dropping all tables and recreating them
    WARNING: This will delete all existing data!
    """
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        print("All tables dropped.")
        
        init_database()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        print("WARNING: This will delete all existing data!")
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        
        if confirm.lower() == 'yes':
            reset_database()
        else:
            print("Database reset cancelled.")
    else:
        init_database()
