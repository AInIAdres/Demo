# KPI Dashboard Autogenerator

Genera KPIs y gráficos desde cualquier CSV y produce un reporte HTML y PNGs usando `matplotlib`. Sin dependencias de APIs externas.

## Casos de uso
- Mostrar valor rápido a un cliente a partir de sus exportaciones (ventas, leads, tickets).
- Entregable visual sin montar BI.

## Requisitos
- Python 3.10+

## Instalación
```bash
pip install -r requirements.txt
```

## Ejecución
```bash
python main.py --csv ./sample_sales.csv --date-col date --value-col amount --group-col channel
```

## Salida
- `output/report.html`
- `output/series.png`
- `output/by_group.png`
