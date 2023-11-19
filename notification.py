
from win10toast import ToastNotifier
# Inicializa # 
toaster = ToastNotifier() 
# # Passa parametros e mostra a notificacao # 


def notify(titulo, mensagem, duration=3):
    toaster.show_toast( 
        titulo,
        mensagem,
        threaded=True, 
        icon_path=None,     
        duration=duration 
    )


if __name__ == "__main__":
    notify("Titulo", "Mensagem", duration=3)