from libraries.connection import connection


# WHILE TRUE
#       Test connection
#       Record log if status was changed
#       Send notification when internet is up again

# Controles:
#       Arquivo de configuração
#       Arquivo de log
print('connected' if connection() else 'no internet!')