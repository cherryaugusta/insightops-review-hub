import { Badge } from "./Badge";

type ScorePillProps = {
  label: string;
  score: string;
  verdict?: "pass" | "review" | "fail";
};

function verdictTone(verdict?: "pass" | "review" | "fail") {
  if (verdict === "pass") return "success";
  if (verdict === "fail") return "danger";
  if (verdict === "review") return "warning";
  return "info";
}

export function ScorePill({ label, score, verdict }: ScorePillProps) {
  return (
    <div className="score-pill">
      <div>
        <div className="score-pill__label">{label}</div>
        <div className="score-pill__value">{score}</div>
      </div>
      {verdict ? <Badge tone={verdictTone(verdict)}>{verdict}</Badge> : null}
    </div>
  );
}
