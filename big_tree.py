import os
import random

import amulet
from amulet.api.block import Block
from amulet.api.chunk import Chunk

os.system("clear")


# load the level
# this will automatically find the wrapper that can open the world and set everything up for you.
level = amulet.load_level(
    "/Users/john/Library/Application Support/minecraft/saves/New Adventure!!"
)

game_version = ("java", (1, 19, 3))  # the version that we want the block data in.

tree_x_offset = 40
tree_y_offset = 70
tree_z_offset = -40

# define the size of the column
tree_width = 14
height = 290
# get the jungle log block
jungle_log = Block("minecraft", "jungle_log")
jungle_stairs = Block("minecraft", "jungle_stairs")
air = Block("minecraft", "air")

stair_lookup = [
    [[3, 0], [2, 0]],
    [[3, -1], [2, -1]],
    [[3, -2], [2, -2], [2, -3]],
    [[1, -2], [1, -3]],
    [[0, -2], [0, -3]],
    [[-1, -2], [-1, -3]],
    [[-2, -2], [-2, -3], [-3, -2]],
    [[-2, -1], [-3, -1]],
    [[-2, 0], [-3, 0]],
    [[-2, 1], [-3, 1]],
    [[-2, 2], [-2, 3], [-3, 2]],
    [[-1, 2], [-1, 3]],
    [[0, 2], [0, 3]],
    [[1, 2], [1, 3]],
    [[2, 2], [2, 3], [3, 2]],
    [[2, 1], [3, 1]],
]

probLookup = {
    32: 0.95,
    34: 0.9,
    36: 0.9,
    37: 0.5,
    40: 0.2,
    41: 0.1,
    45: 0.05,
    49: 0.05,
}


def make_trunk():
    stair_counter = 0
    # place the jungle logs in a column
    for y in range(tree_y_offset, height):
        for x in range(-tree_width // 2, tree_width // 2):
            for z in range(-tree_width // 2, tree_width // 2):
                hypotSq = x**2 + z**2
                if abs(x) == 3 and abs(z) == 3:
                    level.set_version_block(
                        x + tree_x_offset,
                        y,
                        z + tree_z_offset,
                        "minecraft:overworld",  # dimension
                        game_version,
                        jungle_log,
                    )
                elif abs(x) <= 3 and abs(z) <= 3:
                    level.set_version_block(
                        x + tree_x_offset,
                        y,
                        z + tree_z_offset,
                        "minecraft:overworld",  # dimension
                        game_version,
                        air,
                    )
                elif hypotSq < 30:
                    level.set_version_block(
                        x + tree_x_offset,
                        y,
                        z + tree_z_offset,
                        "minecraft:overworld",  # dimension
                        game_version,
                        jungle_log,
                    )
                else:
                    if random.random() < probLookup.get(hypotSq, 0):
                        level.set_version_block(
                            x + tree_x_offset,
                            y,
                            z + tree_z_offset,
                            "minecraft:overworld",  # dimension
                            game_version,
                            jungle_log,
                        )
        # staircase block
        for p in stair_lookup[stair_counter % len(stair_lookup)]:
            level.set_version_block(
                tree_x_offset + p[0],
                y,
                tree_z_offset + p[1],
                "minecraft:overworld",  # dimension
                game_version,
                jungle_log,
            )
        stair_counter += 1


# # save the changes to the world
make_trunk()
level.save()
level.close()

# make branch
def branch_slice(axis, x_origin, y_origin, z_origin):
    is_x = axis == "x"
    for p in [[0, -2], [-1, -1], [-2, 0], [-1, 1], [0, 2], [1, 1], [2, 0], [1, -1]]:
        level.set_version_block(
            x_origin + (p[0] if is_x else 0),
            y_origin + p[1],
            z_origin + (0 if is_x else p[0]),
            "minecraft:overworld",  # dimension
            game_version,
            jungle_log,
        )


def make_branch(axis, direction, startX, startY, startZ, height):
    is_x = axis == "x"
    # NB slice axis is orthogonal to branch axis
    slice_axis = "z" if is_x else "x"
    for ix in range(height):
        delta = direction * ix
        x = startX + delta if is_x else startX
        z = startZ if is_x else startZ + delta
        branch_slice(
            slice_axis,
            x,
            startY + ix,
            z,
        )


# for i in range(18):
#     make_branch(
#         random.choice(["z", "x"]),
#         random.choice([1, -1]),
#         tree_x_offset,
#         tree_y_offset + random.randint(40, 260),
#         tree_z_offset,
#         random.randint(15, 70),
#     )

# # # save the changes to the world
# level.save()
# level.close()
