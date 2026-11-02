from app import create_app, db
from app.models import User, Note

app = create_app()

with app.app_context():

    db.create_all()

    demo_user = User.query.filter_by(
        username="demo_user"
    ).first()

    if demo_user is None:

        demo_user = User(
            username="demo_user",
            email="demo@example.com"
        )

        demo_user.set_password("Password123!")

        db.session.add(demo_user)
        db.session.flush()

    existing_notes = Note.query.filter_by(
        user_id=demo_user.id
    ).first()

    if existing_notes is None:

        notes = [
            Note(
                title="Plan the week",
                content="List important tasks for the week.",
                category="Planning",
                is_completed=False,
                user_id=demo_user.id
            ),

            Note(
                title="Study Flask",
                content="Revise Flask authentication and relationships.",
                category="Education",
                is_completed=True,
                user_id=demo_user.id
            ),

            Note(
                title="Complete project",
                content="Finish the productivity application.",
                category="Work",
                is_completed=False,
                user_id=demo_user.id
            )
        ]

        db.session.add_all(notes)

    db.session.commit()

    print("Database seeded successfully!")
    print("Username: demo_user")
    print("Password: Password123!")