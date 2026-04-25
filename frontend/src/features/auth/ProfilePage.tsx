import { useQuery } from "@tanstack/react-query";
import { fetchMe } from "./api";
import { LoadingState } from "../../components/ui/LoadingState";
import { useAuthStore } from "./store";

export function ProfilePage() {
  const { setUser } = useAuthStore();

  const query = useQuery({
    queryKey: ["me"],
    queryFn: async () => {
      const user = await fetchMe();
      setUser(user);
      return user;
    },
  });

  if (query.isLoading) {
    return <LoadingState label="Loading profile..." />;
  }

  if (!query.data) {
    return <div>Unable to load profile.</div>;
  }

  const user = query.data;

  return (
    <section className="page-section">
      <h1>Profile</h1>
      <div className="detail-card">
        <p><strong>Display name:</strong> {user.display_name}</p>
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>First name:</strong> {user.first_name}</p>
        <p><strong>Last name:</strong> {user.last_name}</p>
      </div>
    </section>
  );
}
