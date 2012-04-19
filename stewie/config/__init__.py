
from pysettings.loaders import mod_to_settings

settings = None
allowed_envs = ['dev', 'qa1', 'prod', 'test']

def load_settings(env):
    global settings

    if env not in allowed_envs:
        raise ValueError("`env` should be in %r" % allowed_envs)

    print 'Using environ: %s' % env
    settings = mod_to_settings('stewie.config.' + env)
