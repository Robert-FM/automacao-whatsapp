from whatsapp_sender import configurar_logs, executar, parse_args


if __name__ == "__main__":
    configurar_logs()
    executar(parse_args())
