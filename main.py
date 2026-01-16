from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def vapi_tool_handler(request: Request):
    # Vapi sends a 'tool-call' message when the LLM triggers a function
    data = await request.json()
    message = data.get("message", {})
    
    if message.get("type") == "tool-call":
        tool_call = message.get("toolCall", {})
        function_name = tool_call.get("function", {}).get("name")
        
        # Example Tool: Get Status
        if function_name == "get_order_status":
            order_id = tool_call.get("function", {}).get("arguments", {}).get("orderId")
            # In a real app, query your DB here
            return {"status": f"Order {order_id} is currently out for delivery!"}

    return {"error": "Unknown tool call"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
