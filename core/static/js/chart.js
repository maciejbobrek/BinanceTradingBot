import * as  ws from "./ws_managment.js";
var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 1000,
  	height: 500,
	layout: {
		backgroundColor: '#363636',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	priceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
		timeVisible: true,
		secondsVisible: false,
	},
});
var candleSeries = chart.addCandlestickSeries({
	upColor: '#00ff00',
	downColor: '#ff0000', 
	borderDownColor: 'rgba(120, 0, 0, 1)',
	borderUpColor: 'rgba(0, 120, 0, 1)',
	wickDownColor: 'rgba(120, 0, 0, 1)',
	wickUpColor: 'rgba(0, 120, 0, 1)',
});

window.candleSeries = candleSeries;
var ws_url = "wss://stream.binance.com:9443/ws/btcusdt@kline_15m";
window.ws_url = ws_url;
var prev_ws_url = ws_url;
window.prev_ws_url = prev_ws_url;
var binanceSocket;
window.binanceSocket = binanceSocket;
ws.initWebSocket();
var symbols_list = document.getElementById("symbol");
var change_ws_url = symbols_list.addEventListener("change", ws.change_stream);
