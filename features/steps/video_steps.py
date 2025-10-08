import asyncio
import grpc
from behave import given, when, then
from aiortc import RTCPeerConnection

import sys
sys.path.insert(0, '..')  
import signaling_pb2
import signaling_pb2_grpc


@given('the server is running on localhost')
def step_server_running(context):
    """Перевіряємо що сервер доступний"""
    context.server_address = 'localhost:50051'
    context.channel = grpc.insecure_channel(context.server_address)
    context.stub = signaling_pb2_grpc.SignalingStub(context.channel)
    

    try:
        grpc.channel_ready_future(context.channel).result(timeout=5)
    except grpc.FutureTimeoutError:
        raise Exception("Server is not running!")


@when('the client sends an OfferMessage')
def step_send_offer(context):
    """Створюємо та відправляємо Offer"""
    async def send_offer():
        pc = RTCPeerConnection()
        pc.addTransceiver("video", direction="recvonly")
        pc.addTransceiver("audio", direction="recvonly")
        
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        
        grpc_offer = signaling_pb2.OfferMessage(
            sdp=pc.localDescription.sdp,
            type=pc.localDescription.type
        )
        
        context.pc = pc
        context.offer = grpc_offer
        
        async with grpc.aio.insecure_channel(context.server_address) as channel:
            stub = signaling_pb2_grpc.SignalingStub(channel)
            context.answer = await stub.SendOffer(grpc_offer)
    
    # Запускаємо async функцію
    asyncio.run(send_offer())


@then('the client should receive an AnswerMessage')
def step_receive_answer(context):
    """Перевіряємо що отримали Answer"""
    assert hasattr(context, 'answer'), "No answer received!"
    assert context.answer.sdp, "Answer SDP is empty!"
    assert context.answer.type == "answer", f"Wrong type: {context.answer.type}"


@when('the client sends a ChatMessage "{message}"')
def step_send_chat_message(context, message):
    """Відправляємо chat повідомлення"""
    async def send_message():
        async with grpc.aio.insecure_channel(context.server_address) as channel:
            stub = signaling_pb2_grpc.SignalingStub(channel)
            chat_message = signaling_pb2.ChatMessage(sender="test_client", text=message)
            context.response = await stub.SendMessage(chat_message)
    
    asyncio.run(send_message())


@then('the server should respond with an echo "{expected_echo}"')
def step_check_echo(context, expected_echo):
    """Перевіряємо echo відповідь"""
    assert hasattr(context, 'response'), "No response received!"
    assert context.response.success == True, "Response not successful!"
    assert context.response.echo == expected_echo, \
        f"Expected echo '{expected_echo}', got '{context.response.echo}'"


@when('the client subscribes to chat stream')
def step_subscribe_to_stream(context):
    """Підписуємось на стрім повідомлень"""
    async def subscribe():
        async with grpc.aio.insecure_channel(context.server_address) as channel:
            stub = signaling_pb2_grpc.SignalingStub(channel)
            chat_message = signaling_pb2.ChatMessage(sender="test_client", text="subscribe")
            
            context.messages = []
            async for msg in stub.StreamMessages(chat_message):
                context.messages.append(msg)
    
    asyncio.run(subscribe())


@then('the client should receive {count:d} messages')
def step_check_message_count(context, count):
    """Перевіряємо кількість отриманих повідомлень"""
    assert hasattr(context, 'messages'), "No messages received!"
    assert len(context.messages) == count, \
        f"Expected {count} messages, got {len(context.messages)}"
    
    expected_texts = ["Hi from server", "What's up", "Please watch video from stream"]
    for i, msg in enumerate(context.messages):
        assert msg.text == expected_texts[i], \
            f"Message {i}: expected '{expected_texts[i]}', got '{msg.text}'"