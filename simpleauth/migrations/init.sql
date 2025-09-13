-- SimpleAuth schema initialization
CREATE TABLE IF NOT EXISTS public.app_client (
    client_id VARCHAR(50) PRIMARY KEY,
    client_secret VARCHAR(255) NOT NULL,
    scope VARCHAR[] DEFAULT ARRAY[]::VARCHAR[]
);

CREATE TABLE IF NOT EXISTS public.token (
    client_id VARCHAR(50) REFERENCES public.app_client(client_id) ON DELETE CASCADE,
    access_scope VARCHAR[],
    access_token VARCHAR(255) UNIQUE NOT NULL,
    expiration_time TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- Example client (password is 'devops-secret' hashed using simple sha256 for demo - but store hashed in production)
INSERT INTO public.app_client (client_id, client_secret, scope)
VALUES ('devops', 'devops-secret', ARRAY['push_send']);