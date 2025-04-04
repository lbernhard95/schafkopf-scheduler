from beachbooker import main, config, gmail


def handler(event, context):
    main.main()
    gmail.send_beachbooker_run_logs(receivers=config.NOTIFICATION_RECEIVER_EMAILS)
