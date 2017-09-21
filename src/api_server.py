from apscheduler.schedulers.background import BackgroundScheduler
from nlp.model.q import q
from nlp.service.tfidf_similarity import TfidfSimilarity
from sanic import Sanic
from sanic.response import json
from sanic import response

app = Sanic()
s = TfidfSimilarity()

def update_model():
    print("Running scheduled update")
    s.update_model()

@app.listener('before_server_start')
def initialize_scheduler(app, loop):
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_model, 'interval', seconds=30)
    scheduler.start()


@app.route("/ask")
async def ask(request):
    q_param = request.args['q'][0]
    question = q(question=q_param)
    results = s.query(question)
    if len(results) == 0:
        s.add_question(question)
        return response.json({
            "message": "Question not found! Will be added to the database now.",
            "question": question.question
        }, status=404)
    else:
        return json(results)

@app.route("/")
async def test(request):
    return json({"number_of_questions": len(s.qs)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=1)