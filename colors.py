# move
snake_position = [300, 300]  # [x->, yv]
snake_body = [[300, 300],
              [290, 300],
              [280, 300]]

# insert
snake_position = [310, 300]  # [x->, yv]
snake_body = [[310, 300],
              [300, 300],
              [290, 300],
              [280, 300]]

# pop
snake_position = [300, 300]  # [x->, yv]
snake_body = [[310, 300],
              [300, 300],
              [290, 300],
              [290, 310]]
# direction des schwanzendes ermitteln
snake_end_last_0 = snake_body[len(snake_body) - 1]
snake_end_last_1 = snake_body[len(snake_body) - 2]

end_direction = ""
# rechts
if snake_end_last_0[0] - 10 == snake_end_last_1[0]:
    end_direction = "right"
# links
elif snake_end_last_0[0] + 10 == snake_end_last_1[0]:
    end_direction = "left"
# oben
elif snake_end_last_0[1] + 10 == snake_end_last_1[1]:
    end_direction = "up"
# unten
elif snake_end_last_0[1] - 10 == snake_end_last_1[1]:
    end_direction = "down"

print(end_direction)

for i in range(0, 4):
    new_element = [snake_body[len(snake_body)-1][0] - 10, snake_body[len(snake_body)-1][1]]
    snake_body.insert(len(snake_body), new_element)

#print(snake_body)
# kreiere list element
# insert snake_body[len(snake_body)-1] an snake_body len
