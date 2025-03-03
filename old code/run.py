from old import create_app
import os
from old.database.models import create_tables
from dotenv import load_dotenv

app = create_app()

if __name__ == '__main__':
    env_file = '.env'
    if not os.path.exists(env_file):
        with open(env_file, 'w') as file:
            file.write(
                "# Discord Bot Token\n"
                "DISCORD_TOKEN=your_discord_token\n\n"
                "# AWS Configuration\n"
                "AWS_ACCESS_KEY_ID=your_aws_access_key_id\n"
                "AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key\n"
                "AWS_REGION_NAME=your_aws_region\n\n"
                "# Database URL\n"
                "DATABASE_URL=sqlite:///./data/database.db\n"
            )
    load_dotenv()
    engine = os.getenv('DATABASE_URL')
    create_tables(engine)
    app.run(debug=True, port=os.getenv('FLASK_RUN_PORT', 5000))
