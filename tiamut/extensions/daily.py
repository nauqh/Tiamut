import hikari
import lightbulb
import os
from datetime import datetime as dt
from apscheduler.triggers.cron import CronTrigger

"""
Schedule daily task 

Contain functions for daily reminder or updates from APIs

:doc: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html
"""

daily_plugin = lightbulb.Plugin("Daily", "⛅ Daily updates utilities")

CHANNEL = int(os.environ["STDOUT_CHANNEL_ID"])


async def msg() -> None:
    await daily_plugin.app.rest.create_message(CHANNEL, "Morning Message\n Here is our today tasks:")


# @daily_plugin.listener(hikari.StartedEvent)
# async def on_started(_: hikari.StartedEvent) -> None:
#     # This event fires once, when the BotApp is fully started.
#     daily_plugin.app.d.sched.add_job(
#         msg, CronTrigger(second=10))


@daily_plugin.command
@lightbulb.option(
    "content", "Reminder content", str, required=True
)
@lightbulb.option(
    "date", "Date of event (dd/mm/yyyy)", str, required=True
)
@lightbulb.command(
    "task", "Add task"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def task(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.user)

    content = ctx.options.content
    date = ctx.options.date

    ctx.bot.d.db.execute("INSERT INTO task (task_memid, task_content, task_date) VALUES (?, ?, ?)",
                         target.id, content, date)
    ctx.bot.d.db.commit()

    await ctx.respond(f"{target.mention} task is added")


@daily_plugin.command
@lightbulb.command(
    "mytask", "Show member task"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def task(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.user)

    resp = ctx.bot.d.db.records(
        f"SELECT * FROM task WHERE task_memid = {target.id}")

    embed = (
        hikari.Embed(
            title=f"{target.display_name} - Task",
            description=f"`ID: {target.id}`",
            colour=0x181818,
            timestamp=dt.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_thumbnail(target.avatar_url or target.default_avatar_url)
    )

    reminder = {}
    for item in resp:
        date = item[3]
        reminder[date] = []

    for item in resp:
        date = item[3]
        task = item[2]
        reminder[date] += [task]

    days = []
    jobs = []
    for date in reminder:
        job = ""
        for task in reminder[date]:
            job += f"- {task}\n"
        jobs.append(job)
        days.append(date)

    for i in range(len(days)):
        embed.add_field(
            f"📌 - {days[i]}",
            str(jobs[i]),
            inline=False
        )

    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(daily_plugin)
