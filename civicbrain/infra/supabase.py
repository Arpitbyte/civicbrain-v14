"""Supabase Admin Client provider."""

from supabase import Client, create_client

from civicbrain.infra.config import settings


def get_supabase_admin_client() -> Client:
    """Returns initialized Supabase Admin Client using service role key."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
