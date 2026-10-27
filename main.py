import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    input_tipo = ft.TextField(label="Tipo", expand=True)
    input_marca = ft.TextField(label="Marca", expand=True)
    input_anno = ft.TextField(label="Anno acquisto", expand=True)

    txt_valore = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=70)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def minus_click(e):
        try:
            valore_corrente = int(txt_valore.value)
            if valore_corrente > 0:
                txt_valore.value = str(valore_corrente - 1)
                page.update()
        except ValueError:
            pass

    def plus_click(e):
        try:
            valore_corrente = int(txt_valore.value)
            txt_valore.value = str(valore_corrente + 1)
            page.update()
        except ValueError:
            pass

    def aggiungi_strumento_click(e):
        # Controlliamo che i campi non siano vuoti
        if not input_tipo.value or not input_marca.value or not input_anno.value or not txt_valore.value:
            alert.show_alert("Errore: Compila tutti i campi prima di aggiungere uno strumento.")
            return

        # Validazione campi numerici
        try:
            anno = int(input_anno.value)
            valore = float(txt_valore.value)

            if anno > 2026:
                alert.show_alert("Errore: L'anno di acquisto non può essere successivo al 2026.")
                return
        except ValueError:
            alert.show_alert("Errore: L'anno di acquisto e il valore devono essere valori numerici validi.")
            return

        try:
            # Aggiungiamo lo strumento al deposito
            deposito.aggiungi_strumento(input_tipo.value, input_marca.value, anno, valore)

            # Svuotiamo i campi
            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            txt_valore.value = "0"

            # Aggiorniamo la UI
            aggiorna_lista_strumenti()
        except Exception as ex:
            alert.show_alert(f"Errore durante l'inserimento: {ex}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btn_minus = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red", on_click=minus_click)
    btn_plus = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", on_click=plus_click)
    btn_aggiungi_strumento = ft.FilledTonalButton("Aggiungi strumento", on_click=aggiungi_strumento_click)

    # --- LAYOUT ---
    page.add(
        ft.Row([toggle_cambia_tema], alignment=ft.MainAxisAlignment.START),
        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 3
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(
            controls=[
                input_tipo,
                input_marca,
                input_anno,
                btn_minus,
                txt_valore,
                btn_plus
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        btn_aggiungi_strumento,
        ft.Divider(),

        # Sezione 4
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()


ft.run(main)