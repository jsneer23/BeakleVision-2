import { createFileRoute } from "@tanstack/react-router"
import { Box, Heading, Text } from "@chakra-ui/react"

import { type Match, type Team, TeamService } from "@/client"

export const Route = createFileRoute('/team/$teamNumber/{-$year}')({
  component: TeamPage,
  loader: async ({ params }) => {
    const year = params.year ?? 2025
    const team_key: string = `frc${params.teamNumber}`
    const [
      team,
      events,
      matches
    ]: [Team, string[], Match[]] = await Promise.all([
      TeamService.getTeamByKey({ key: team_key }),
      TeamService.getEventsByYear({ key: team_key, year: year }),
      TeamService.getMatchesByYear({ teamKey: team_key, year: year })
    ])
    return { Team: team, Events: events, Matches: matches }
  },
})

// Define the component that will be rendered for this route
async function TeamPage() {

  const { year } = Route.useParams()
  const { Team: team, Events: events } = Route.useLoaderData()
  return (
    <Box p={8}>
      <Heading mb={4}>Team {team.number} - {team.nickname}</Heading>
      <Text mb={4}> {team.city}, {team.state_prov}, {team.country} </Text>
      <Text mb={4}> Rookie year: {team.rookie_year} </Text>
      <Text mb={4}> Events: {events.join(", ")} </Text>
    </Box>
  )
}