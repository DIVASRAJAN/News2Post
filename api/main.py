from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

# from your_agent_module import create_react_agent, llm, news2post, system_prompt
from api.agent import agent_creation

app = FastAPI(
    title="News to LinkedIn Post Generator",
    description="Generate professional LinkedIn posts from trending news on a given topic.",
    version="1.0.0"
)

# === Input and Output Schemas ===

class TopicRequest(BaseModel):
    topic: str

class PostResponse(BaseModel):
    topic: str
    news_sources: List[str]
    linkedin_post: str
    image_suggestion: Optional[str] = None


# === FastAPI Endpoint ===

@app.post("/generate-post", response_model=PostResponse)
def generate_post(request: TopicRequest):
    try:
        # Build input format for agent
        user_input = request.topic

        print("inputttttttttttttttttt",user_input)

        # Call your agent function
        result = agent_creation(user_input)

        if isinstance(result, str):
            import json
            result = json.loads(result)  # Make sure your agent returns JSON-serializable content

        return PostResponse(
            topic=request.topic,
            news_sources=result.get("links", []),
            linkedin_post=result.get("post", "No content generated."),
            # image_suggestion=result.get("image_suggestion", None)
        )

    except Exception as e:
        logging.exception("Error in generating post")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)