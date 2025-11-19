def human_local_time(dt):
    local_time = timezone.localtime(dt)
    return local_time.strftime("%d.%m.%Y в %H:%М")
    