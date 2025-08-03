# !pip install ipywidgets numpy matplotlib seaborn pandas

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from IPython.display import display, clear_output
import ipywidgets as widgets
import seaborn as sns
import pandas as pd

# --- PARÂMETROS DA SIMULAÇÃO ---
GRID_SIZE = 30
FRAME_COUNT_DEFAULT = 225
RADIUS_DEFAULT = 4

# --- SETUP INICIAL ---
sns.set(style="whitegrid")

# Inicialização do grid (universo observado)
grid_inicial = np.random.choice([0] * 85 + [1] * 15, size=(GRID_SIZE, GRID_SIZE))
energia_inicial_percentual = np.count_nonzero(grid_inicial > 0) / grid_inicial.size * 100
cor_manifestacao = "#440154"
cmap_custom = ListedColormap(['white', cor_manifestacao])

def compute_harmonic_entropy(grid):
    """Calcula Entropia Harmônica: EH = 1 - |2p - 1|"""
    p = np.count_nonzero(grid > 0) / grid.size
    EH = 1 - abs(2*p - 1)
    return EH, p

def classify_harmonic_state(EH, p):
    """Classifica estado do sistema baseado na Entropia Harmônica"""
    if EH < 0.3:
        if p < 0.2:
            return "Harmonia Vazia"
        else:
            return "Harmonia Plena"
    elif EH > 0.7:
        return "Caos Máximo"
    else:
        return "Transição Entrópica"

def activate(grid, x, y, radius):
    """Ativa as células na área de percepção do Observador."""
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                grid[nx, ny] = 1
    return grid

def compute_manifestation_cost(grid_before, x, y, radius):
    """Calcula o Custo de Manifestação Instantâneo."""
    activated_region = [
        (x + dx, y + dy)
        for dx in range(-radius, radius + 1)
        for dy in range(-radius, radius + 1)
        if 0 <= x + dx < grid_before.shape[0] and 0 <= y + dy < grid_before.shape[1]
    ]
    newly_activated_count = sum(1 for nx, ny in activated_region if grid_before[nx, ny] == 0)
    return newly_activated_count / grid_before.size

def animate(frame_count, compressao_harmonica_percent, activation_radius):
    """Executa a animação e os cálculos com Entropia Harmônica."""
    grid = grid_inicial.copy()

    energia_total_acumulada = []
    custo_bruto_manifestacao = []
    energia_parcimoniosa_final = []
    entropia_harmonica_timeline = []
    proporcao_timeline = []
    estado_timeline = []

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    fig.suptitle("HIPÓTESE UNIVERSAL DA MANIFESTAÇÃO HARMÔNICA - HUMH", fontsize=20, fontweight='bold')

    # Configuração do grid visual
    img = ax1.imshow(grid, cmap=cmap_custom, vmin=0, vmax=1, aspect='equal', origin='lower')
    # O título agora será definido dentro do loop para ser dinâmico

    # Setup do gráfico de energia
    plot_total, = ax2.plot([], [], lw=2.5, color='gray', alpha=0.7, label="Energia Total (Realista)")
    plot_bruto, = ax2.plot([], [], lw=2, color='darkorange', linestyle='--', label="Custo Bruto (Parcimônia)")
    plot_parcimoniosa, = ax2.plot([], [], lw=2.5, color='deepskyblue', label="Energia Final (HUMH)")
    ax2.axhline(energia_inicial_percentual, color='gold', linestyle='--', lw=2, label="Energia Inicial")
    ax2.set_xlim(0, frame_count)
    ax2.set_ylim(0, 100)
    ax2.set_title(f"Análise Energética (CH: {compressao_harmonica_percent}%)")
    ax2.set_xlabel("Iterações")
    ax2.set_ylabel("Energia Funcional (%)")
    ax2.legend(loc='upper left')

    # Setup do gráfico de Entropia Harmônica
    plot_eh, = ax3.plot([], [], lw=3, color='purple', label="Entropia Harmônica")
    ax3.axhline(0, color='green', linestyle='-', alpha=0.3, label="Harmonia Perfeita (EH=0)")
    ax3.axhline(1, color='red', linestyle='-', alpha=0.3, label="Caos Máximo (EH=1)")
    ax3.set_xlim(0, frame_count)
    ax3.set_ylim(-0.05, 1.1)
    ax3.set_title("Evolução da Entropia Harmônica")
    ax3.set_xlabel("Iterações")
    ax3.set_ylabel("Entropia Harmônica (EH)")
    ax3.legend(loc='upper left')

    # Setup do gráfico de proporção
    plot_prop, = ax4.plot([], [], lw=2.5, color='orange', label="Proporção Manifestada (p)")
    ax4.axhline(0, color='blue', linestyle='--', alpha=0.5, label="Harmonia Vazia (p=0)")
    ax4.axhline(1, color='red', linestyle='--', alpha=0.5, label="Harmonia Plena (p=1)")
    ax4.axhline(0.5, color='black', linestyle=':', alpha=0.7, label="Pico do Caos (p=0.5)")
    ax4.set_xlim(0, frame_count)
    ax4.set_ylim(-0.05, 1.1)
    ax4.set_title("Proporção de Manifestação")
    ax4.set_xlabel("Iterações")
    ax4.set_ylabel("Proporção (p)")
    ax4.legend(loc='upper left')

    for i in range(frame_count):
        x = int((np.sin(i / 15) + 1) / 2 * GRID_SIZE)
        y = int((np.cos(i / 20) + 1) / 2 * GRID_SIZE)

        grid_before = grid.copy()
        grid = activate(grid, x, y, activation_radius)

        total_ratio = np.count_nonzero(grid > 0) / grid.size * 100
        energia_total_acumulada.append(total_ratio)

        manifestation_cost = compute_manifestation_cost(grid_before, x, y, activation_radius) * 100
        custo_bruto_manifestacao.append(manifestation_cost)

        fator_compressao = 1 - (compressao_harmonica_percent / 100)
        parsimonious_energy = manifestation_cost * fator_compressao
        energia_parcimoniosa_final.append(parsimonious_energy)

        EH, p = compute_harmonic_entropy(grid)
        estado_atual = classify_harmonic_state(EH, p)
        
        entropia_harmonica_timeline.append(EH)
        proporcao_timeline.append(p)
        estado_timeline.append(estado_atual)

        # --- ATUALIZAÇÃO DOS GRÁFICOS ---
        img.set_data(grid)
        for patch in reversed(ax1.patches):
            patch.remove()

        # --- ALTERAÇÃO AQUI ---
        # Define o título da grade dinamicamente a cada iteração
        ax1.set_title(f"Iteração: {i+1}/{frame_count} | Raio: {activation_radius}")

        circ = plt.Circle((y, x), radius=activation_radius, edgecolor='red', facecolor='none', lw=1.5, alpha=0.7)
        ax1.add_patch(circ)
        
        ax1.text(0.02, 0.98, f"Estado: {estado_atual}", transform=ax1.transAxes, 
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                 verticalalignment='top', fontsize=10, fontweight='bold')

        plot_total.set_data(range(len(energia_total_acumulada)), energia_total_acumulada)
        plot_bruto.set_data(range(len(custo_bruto_manifestacao)), custo_bruto_manifestacao)
        plot_parcimoniosa.set_data(range(len(energia_parcimoniosa_final)), energia_parcimoniosa_final)
        
        plot_eh.set_data(range(len(entropia_harmonica_timeline)), entropia_harmonica_timeline)
        plot_prop.set_data(range(len(proporcao_timeline)), proporcao_timeline)

        fig.tight_layout(rect=[0, 0, 1, 0.96])
        
        clear_output(wait=True)
        display(fig)
        plt.pause(0.05)

        if np.all(grid > 0):
            print("Universo totalmente manifestado - Harmonia Plena alcançada.")
            break

    plt.close(fig)

    # (O código para o relatório final continua o mesmo)
    EH_inicial, p_inicial = compute_harmonic_entropy(grid_inicial)
    EH_final, p_final = compute_harmonic_entropy(grid)
    media_parcimonia_final = np.mean(energia_parcimoniosa_final)
    media_custo_bruto = np.mean(custo_bruto_manifestacao)

    print(f"\n{'='*60}")
    print(f"RELATÓRIO FINAL - VALIDAÇÃO COMPUTACIONAL (Raio: {activation_radius})")
    print(f"{'='*60}")
    print(f"Compressão Harmônica aplicada: {compressao_harmonica_percent}%")
    print(f"Frames simulados: {len(entropia_harmonica_timeline)}")
    print(f"\nTRAJETÓRIA ENTRÓPICA:")
    print(f"• EH inicial: {EH_inicial:.4f} (p = {p_inicial:.3f}) - {classify_harmonic_state(EH_inicial, p_inicial)}")
    print(f"• EH final: {EH_final:.4f} (p = {p_final:.3f}) - {classify_harmonic_state(EH_final, p_final)}")
    if EH_inicial > 0:
        print(f"• Redução da Entropia Harmônica: {((EH_inicial - EH_final)/EH_inicial*100):.1f}%")
    
    if p_final > 0.9:
        print(f"\n✓ VALIDAÇÃO: Sistema evoluiu para Harmonia Plena conforme previsto pela HUMH")
    else:
        print(f"\nOBSERVAÇÃO: Sistema em trânsito para a Harmonia Plena.")
    
    print(f"\nEFICIÊNCIA ENERGÉTICA:")
    print(f"• Modelo Realista (energia total): {energia_total_acumulada[-1]:.1f}%")
    print(f"• Parcimônia Pura (custo bruto médio): {media_custo_bruto:.3f}%")
    print(f"• HUMH Completa (energia final média): {media_parcimonia_final:.3f}%")
    if media_custo_bruto > 0:
      print(f"• Economia da HUMH (Compressão): {((media_custo_bruto - media_parcimonia_final)/media_custo_bruto*100):.1f}%")
    
    print(f"\n{'='*60}")

# --- INTERFACE INTERATIVA FINAL ---
frame_slider = widgets.IntSlider(value=FRAME_COUNT_DEFAULT, min=10, max=1000, step=10, description="Nº de Frames:")
compression_slider = widgets.FloatSlider(value=70.0, min=0.0, max=100.0, step=1.0, description="Compressão Harmônica (%):")
radius_slider = widgets.IntSlider(value=RADIUS_DEFAULT, min=1, max=10, step=1, description="Raio de Ativação:")
start_button = widgets.Button(description="▶ Iniciar Simulação HUMH", button_style='success')

info_text = widgets.HTML(value="""
<div style='background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin: 10px 0;'>
<h3 style='color: #4169e1; margin-top: 0;'>🔬 SIMULAÇÃO HUMH</h3>
<p>Esta simulação valida os princípios da HUMH, mostrando a evolução de um universo derivado sob a percepção de um Observador.</p>
</div>
""")

def on_button_click(b):
    clear_output(wait=True)
    display(ui)
    animate(frame_slider.value, compression_slider.value, radius_slider.value)

start_button.on_click(on_button_click)

ui = widgets.VBox([info_text, frame_slider, compression_slider, radius_slider, start_button])
display(ui)