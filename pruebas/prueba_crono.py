def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    f_minutes = f'{minutes:02}'
    f_seconds = f'{seconds:02}'
    #return f'{minutes:02}:{seconds:02}'
    return f'{f_minutes}:{f_seconds}'
