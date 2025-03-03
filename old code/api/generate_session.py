import uuid
from flask import request, jsonify
from sqlalchemy import func

from old.database.database import get_session
from old.database.models import Line, Template, Theme

def generate_session():
    """
    Generates a hypnosis session based on user preferences and session parameters.

    Expected Input (JSON Payload):
    {
        "user_id": Optional[int],
        "themes": Optional[List[str]],
        "duration": Optional[int],  # in minutes
        "difficulty": Optional[str],
        "dominant_name": Optional[str],
        "subject_name": Optional[str],
        "sub_pov": Optional[str],
        "dom_pov": Optional[str],
        "starting_phase": Optional[str]
    }

    Input Parameters:
    - user_id: User's unique identifier.
    - themes: List of themes for the session (e.g., ["empty", "submission"]). Defaults to all themes if not provided.
    - duration: Desired session duration in minutes (default: 15).
    - difficulty: Desired difficulty level (e.g., "MODERATE", default: "MODERATE").
    - dominant_name: Name of the dominant (default: "Master").
    - subject_name: Name of the subject (default: "Slave").
    - sub_pov: Subject's point of view (e.g., "1PS", default: "1PS").
    - dom_pov: Dominant's point of view (e.g., "2PS", default: "2PS").
    - starting_phase: Starting phase type (e.g., "INDUCTION"), optional.

    Output (JSON Response):
    {
        "session_id": str,
        "status": str,
        "phases": List[Phase]
    }

    Each Phase is a dictionary:
    {
        "phase_type": str,
        "objectives": List[str],
        "difficulty": str,
        "duration": int,  # in seconds
        "audio_lines": List[AudioLine],
        "subliminal_texts": List[str],
        "images": List[str],
        "binaural_url": str,
        "frequency": float  # in Hz
    }

    Each AudioLine is a dictionary:
    {
        "text": str,
        "audio_url": str,
        "duration": int,  # in seconds
        "line_type": str
    }
    """
    data = request.get_json()

    # Extract input variables with defaults
    user_id = data.get('user_id')
    themes = data.get('themes', [])
    duration = data.get('duration', 15)  # in minutes
    difficulty = data.get('difficulty', 'MODERATE')
    dominant_name = data.get('dominant_name', 'Master')
    subject_name = data.get('subject_name', 'Slave')
    sub_pov = data.get('sub_pov', '1PS')
    dom_pov = data.get('dom_pov', '2PS')
    starting_phase = data.get('starting_phase')  # Optional

    # Database session
    db_session = get_session()

    # If no themes provided, use all themes
    if not themes:
        themes = [theme.name for theme in db_session.query(Theme).all()]

    # Initialize phases
    phases = []

    total_duration_seconds = duration * 60  # Convert to seconds
    elapsed_time = 0

    # Define the sequence of phases
    # Adjust or extend this sequence based on your requirements
    default_phase_sequence = [
        {'phase_type': 'INDUCTION', 'duration': 180},  # 3 minutes
        {'phase_type': 'DEEPENER', 'duration': 120},   # 2 minutes
        {'phase_type': 'SUGGESTION_IDENTITY', 'duration': 300},  # 5 minutes
        {'phase_type': 'SUGGESTION_FEELING', 'duration': 300},   # 5 minutes
        {'phase_type': 'EMERGENCE', 'duration': 60}    # 1 minute
    ]

    # Adjust durations proportionally if total duration differs
    total_default_duration = sum([phase['duration'] for phase in default_phase_sequence])
    scaling_factor = total_duration_seconds / total_default_duration

    for phase_def in default_phase_sequence:
        phase_duration = int(phase_def['duration'] * scaling_factor)
        phase_type = phase_def['phase_type']

        # Fetch lines for the phase
        lines_query = db_session.query(Line).join(Template).join(Theme).filter(
            Template.line_type == phase_type,
            Template.difficulty == difficulty,
            Theme.name.in_(themes)
        )

        # Apply user preferences
        if dominant_name:
            lines_query = lines_query.filter(Line.dominant == dominant_name)
        if subject_name:
            lines_query = lines_query.filter(Line.subject == subject_name)
        if sub_pov:
            lines_query = lines_query.filter(Line.sub_pov == sub_pov)
        if dom_pov:
            lines_query = lines_query.filter(Line.dom_pov == dom_pov)

        # Randomize the order
        lines_query = lines_query.order_by(func.random())

        # Handle different phase types
        if phase_type in ['INDUCTION', 'DEEPENER', 'EMERGENCE']:
            # Get a single line
            line = lines_query.first()
            if not line:
                # If no line found, skip this phase
                continue

            audio_lines = [{
                'text': line.real_text,
                'audio_url': line.audio_file_path,
                'duration': int(line.audio_length) if line.audio_length else phase_duration,
                'line_type': line.line_type.value
            }]
            subliminal_texts = []
            images = ['/static/images/default.jpg']  # Placeholder image
        else:
            # For suggestion phases, get multiple lines
            lines = lines_query.all()
            # Limit the number of lines based on phase duration (assuming 10 seconds per line)
            max_lines = phase_duration // 10
            selected_lines = lines[:max_lines]
            audio_lines = []
            subliminal_texts = []
            images = []
            for line in selected_lines:
                audio_lines.append({
                    'text': line.real_text,
                    'audio_url': line.audio_file_path,
                    'duration': int(line.audio_length) if line.audio_length else 10,
                    'line_type': line.line_type.value
                })
                subliminal_texts.append(line.real_text)
                images.append('/static/images/default.jpg')  # Placeholder image

        # Determine binaural frequency based on phase_type
        if phase_type == 'INDUCTION':
            frequency = 8.0  # Alpha waves
            binaural_url = '/static/audio/binaural_alpha.mp3'
        elif phase_type == 'DEEPENER':
            frequency = 4.0  # Theta waves
            binaural_url = '/static/audio/binaural_theta.mp3'
        elif phase_type.startswith('SUGGESTION'):
            frequency = 6.0  # Low alpha/high theta
            binaural_url = '/static/audio/binaural_suggestion.mp3'
        elif phase_type == 'EMERGENCE':
            frequency = 12.0  # Beta waves
            binaural_url = '/static/audio/binaural_beta.mp3'
        else:
            frequency = 8.0  # Default to alpha waves
            binaural_url = '/static/audio/binaural_default.mp3'

        # Create the phase dictionary
        phase = {
            'phase_type': phase_type,
            'objectives': [phase_type.replace('_', ' ').title()],
            'difficulty': difficulty,
            'duration': phase_duration,
            'audio_lines': audio_lines,
            'subliminal_texts': subliminal_texts,
            'images': images,
            'binaural_url': binaural_url,
            'frequency': frequency
        }

        phases.append(phase)
        elapsed_time += phase_duration
        if elapsed_time >= total_duration_seconds:
            break

    # Adjust the last phase's duration if we've exceeded total duration
    if elapsed_time > total_duration_seconds and phases:
        excess_time = elapsed_time - total_duration_seconds
        phases[-1]['duration'] -= excess_time
        if phases[-1]['duration'] < 0:
            phases[-1]['duration'] = 0

    # Generate a session ID
    session_id = str(uuid.uuid4())

    # Build the response
    response = {
        'session_id': session_id,
        'status': 'Session generated successfully.',
        'phases': phases
    }

    return jsonify(response)
