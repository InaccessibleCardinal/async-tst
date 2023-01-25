import asyncio
import random
import time

from consts import accounts


async def delay():
    await asyncio.sleep(random.randint(1, 3))


async def describe_images(account):
    await delay()
    return account["images"]


async def delete_snapshot(snapshot: str):
    await delay()
    print(f"deleting snaphot: {snapshot}")


async def deregister_image(image: str):
    await delay()
    print(f"deregistering {image['ImageId']}")


async def do_deletion(image):
    snapshots = image["snapshots"]

    await asyncio.gather(
        *[deregister_image(image)]
        + [delete_snapshot(snapshot) for snapshot in snapshots]
    )


async def do_work(account):
    images = await describe_images(account)
    print(f"images found for account {account['id']}:\n{images}")
    await asyncio.gather(*[do_deletion(image) for image in images])


def job(accounts):
    for account in accounts:
        asyncio.run(do_work(account))


def main():
    start = time.perf_counter()
    job(accounts=accounts)
    end = time.perf_counter()
    print(f"duration: {end - start}")


if __name__ == "__main__":
    main()
