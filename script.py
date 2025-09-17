import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


os.environ['KIVY_GL_BACKEND'] = 'gl'


class GestorTarefasApp(App):
    def build(self):
        layout_principal = BoxLayout(orientation='vertical')
        layout_input = BoxLayout(orientation='horizontal', size_hint_y=0.1)

        self.input_tarefa = TextInput(hint_text='Digite uma nova tarefa aqui...')
        botao_adicionar = Button(text='Adicionar', size_hint_x=0.3)
        botao_adicionar.bind(on_press=self.adicionar_tarefa)

        layout_input.add_widget(self.input_tarefa)
        layout_input.add_widget(botao_adicionar)

        scroll_view_tarefas = ScrollView()
        self.layout_lista_tarefas = BoxLayout(orientation='vertical', size_hint_y=None)
        self.layout_lista_tarefas.bind(minimum_height=self.layout_lista_tarefas.setter('height'))
        scroll_view_tarefas.add_widget(self.layout_lista_tarefas)

        layout_principal.add_widget(layout_input)
        layout_principal.add_widget(scroll_view_tarefas)

        
        self.carregar_tarefas()

        return layout_principal

    def carregar_tarefas(self, *args):
        
        try:
            if not os.path.exists("tarefas.json"):
                return  # Ficheiro não existe, não faz nada

            with open("tarefas.json", "r") as f:
                if os.path.getsize("tarefas.json") == 0:
                    return  # Ficheiro está vazio, não faz nada

                lista_de_tarefas = json.load(f)

            for texto_tarefa in lista_de_tarefas:
                tarefa_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                texto_da_tarefa = Label(text=texto_tarefa)
                botao_remover = Button(text='X', size_hint_x=0.1)

                tarefa_layout.add_widget(texto_da_tarefa)
                tarefa_layout.add_widget(botao_remover)

                self.layout_lista_tarefas.add_widget(tarefa_layout)
                botao_remover.bind(on_press=lambda instance, layout=tarefa_layout: self.remover_tarefa(layout))

        
        except Exception as e:
           
            print(f"DEBUG: OCORREU UM ERRO AO CARREGAR AS TAREFAS: {e}")

    def salvar_tarefas(self, *args):
        try:
            lista_de_tarefas = []
            for tarefa_layout in self.layout_lista_tarefas.children:
                texto_da_tarefa = tarefa_layout.children[1].text
                lista_de_tarefas.append(texto_da_tarefa)
            lista_de_tarefas.reverse()

            with open("tarefas.json", "w") as f:
                json.dump(lista_de_tarefas, f)
        except Exception as e:
            print(f"DEBUG: OCORREU UM ERRO AO SALVAR AS TAREFAS: {e}")

    def adicionar_tarefa(self, instance):
        tarefa_texto = self.input_tarefa.text
        if tarefa_texto:
            # ... (código para adicionar widget visual) ...
            tarefa_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            texto_da_tarefa = Label(text=tarefa_texto)
            botao_remover = Button(text='X', size_hint_x=0.1)
            tarefa_layout.add_widget(texto_da_tarefa)
            tarefa_layout.add_widget(botao_remover)
            self.layout_lista_tarefas.add_widget(tarefa_layout)
            botao_remover.bind(on_press=lambda instance, layout=tarefa_layout: self.remover_tarefa(layout))
            self.input_tarefa.text = ""

            self.salvar_tarefas()

    def remover_tarefa(self, tarefa_layout):
        self.layout_lista_tarefas.remove_widget(tarefa_layout)
        self.salvar_tarefas()


# A linha para executar a app continua a mesma
if __name__ == '__main__':
    GestorTarefasApp().run()
