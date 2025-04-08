# MCP CLI GUI

Una semplice interfaccia web per interagire con l'API MCP CLI, implementata in Next.js.

## Caratteristiche

- Gestione dei server MCP (aggiunta, rimozione, visualizzazione)
- Esecuzione di query sui server MCP
- Visualizzazione degli strumenti disponibili su ciascun server
- Importazione/esportazione della configurazione
- Interfaccia moderna e reattiva

## Prerequisiti

- Node.js 18 o superiore
- Un server MCP CLI API funzionante

## Installazione

```bash
# Clona il repository
git clone https://github.com/yourusername/mcp-cli-gui.git
cd mcp-cli-gui

# Installa le dipendenze
npm install

# Avvia il server di sviluppo
npm run dev
```

## Configurazione

Per impostazione predefinita, l'applicazione si connette a un server MCP CLI API all'indirizzo `http://localhost:8000/api`. Per modificare questo URL, puoi modificare il file `src/lib/api-client.ts`.

```typescript
// Modifica questo valore per puntare al tuo server MCP CLI API
const baseUrl = 'http://localhost:8000/api';
```

## Utilizzo

### Gestione dei server

Nella sezione "Servers", puoi:
- Visualizzare l'elenco dei server MCP configurati
- Aggiungere nuovi server specificando nome, comando, argomenti e variabili d'ambiente
- Rimuovere i server esistenti

### Esecuzione di query

Nella sezione "Query", puoi:
- Selezionare un server MCP tra quelli configurati
- Specificare il modello da utilizzare (predefinito: gpt-3.5-turbo)
- Inserire una query da eseguire
- Visualizzare il risultato dell'esecuzione

### Visualizzazione degli strumenti

Nella sezione "Tools", puoi:
- Selezionare un server MCP 
- Visualizzare l'elenco degli strumenti disponibili su quel server
- Espandere ciascuno strumento per vedere la descrizione e i parametri richiesti

### Gestione della configurazione

Nella sezione "Configuration", puoi:
- Importare una configurazione esistente da un file
- Esportare la configurazione corrente in un file

## Sviluppo

### Struttura del progetto

```
src/
├── app/                 # Pagine Next.js (app router)
├── components/          # Componenti React
│   ├── ui/              # Componenti UI riutilizzabili
│   └── ...              # Componenti specifici dell'applicazione
├── lib/                 # Librerie e utilità
└── ...
```

### Comandi

```bash
# Avvia il server di sviluppo
npm run dev

# Costruisci l'applicazione per la produzione
npm run build

# Avvia l'applicazione in modalità produzione
npm start

# Esegui il linting
npm run lint
```

## Licenza

MIT
