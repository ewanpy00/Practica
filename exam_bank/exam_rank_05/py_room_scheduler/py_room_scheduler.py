def py_room_scheduler(meetings: list[list[int]]) -> dict:
    if not meetings:
        return {"total_rooms": 0, "schedule": []}

    rooms = []

    for meeting in sorted(meetings, key=lambda m: m[0]):
        start, _ = meeting
        for room in rooms:
            if room[-1][1] <= start:
                room.append(meeting)
                break
        else:
            rooms.append([meeting])

    return {"total_rooms": len(rooms), "schedule": rooms}

# print(py_room_scheduler([[0, 30], [5, 10], [15, 20]]))
# print(py_room_scheduler([]))
