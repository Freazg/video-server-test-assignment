# 🎬 Video Server Test Assignment

## 📋 Overview
Test assignment for **Video Team - Dev in Test** position.

This project implements a gRPC server that streams encrypted video to clients using WebRTC, with full chat functionality and comprehensive BDD testing.

---

##  Completed Tasks

### 1. Docker Container Setup
-  Built working Docker container
-  Fixed missing `sample.mp4.enc` file
-  Server runs on port 50051
-  All dependencies included

### 2. gRPC Code Generation
-  Generated `signaling_pb2.py` (message classes)
-  Generated `signaling_pb2_grpc.py` (service stubs)
-  Updated to grpcio 1.75.1

### 3. Server Bug Fix
**Problem Found:** Missing audio track in video stream

**Solution:**
- Added audio track in `server.py` SendOffer method
- Added audio transceiver in `client.py`
- Video now streams with audio 

### 4. Behave Step Definitions
-  Implemented all step definitions
-  All 3 scenarios passing
-  9/9 steps successful
-  Execution time: ~8 seconds

---
