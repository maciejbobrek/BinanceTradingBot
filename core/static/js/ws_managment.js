/**
 * Changes the stream that the socket fetching data for the lightweight chart 
 */
export function change_stream(){
	prev_ws_url = ws_url;
	ws_url = "wss://stream.binance.com:9443/ws/";
	ws_url += document.getElementById("symbol").value.toLowerCase();
	ws_url += "@kline_15m";
	console.log(binanceSocket);
	binanceSocket.close();
	initWebSocket();
}

export function initWebSocket(){
	console.log("Init BinanceWS:", ws_url);
	binanceSocket = new WebSocket(ws_url);
	binanceSocket.onmessage = parse_exchrate_data;
	binanceSocket.onclose = Onclose;
	set_hist_data();
}
/**
 * Fetches candlestick data and parses it to the lightweight chart
 */
export function set_hist_data(){
    fetch(document.location.origin+'/chart_history', {method: 'POST', body:JSON.stringify(ws_url)})
	.then((r) => r.json())
	.then((response) => {
		candleSeries.setData(response);
    })
}

export function Onclose(){
	console.log("Closed BinanceWS:",prev_ws_url);
}

/**
 * Processes the messages received by the websocket to a lightweightchart data type
 * @param {JSON} event raw candlestick data: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
 */
 export function parse_exchrate_data(event) {	
	var message = JSON.parse(event.data);

	var candlestick = message.k;
	console.log(candlestick)

	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}